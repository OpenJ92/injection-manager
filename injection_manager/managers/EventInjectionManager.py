from asyncio import gather, Event

from injection_manager.typeclass.Injectable import Injectable
from injection_manager.typeclass.Session import AsyncSession

class EventInjectionManager:
    def __init__(self, base):
        """
        Initialize the EventInjectionManager.
        :param base: SQLAlchemy Base, providing metadata and injectable models.
        """
        self.base = base
        self.metadata = base.metadata
        self.events = {}  # Dictionary to track events for each table

    def _get_event(self, table_name):
        """
        Retrieve or create an asyncio.Event for a specific table.
        :param table_name: Fully qualified table name (e.g., schema.table).
        :return: asyncio.Event instance.
        """
        if table_name not in self.events:
            self.events[table_name] = Event()
        return self.events[table_name]

    async def inject(self, data, session: AsyncSession):
        """
        Perform the injection process using Event-based synchronization.
        :param data: Parsed data object to inject.
        :param session: Database session supporting flush, commit, and rollback.
        """
        tasks = []
        for name, relation in self.metadata.tables.items():
            ORM_Injectable = self.base.injectable.get(name)
            if ORM_Injectable:
                # Define dependencies from the class relationships
                dependencies = []
                for dependency in relation.foreign_key_constraints:
                    fkey = f"{dependency.referred_table.schema}.{dependency.referred_table.name}"
                    dependencies.append(fkey)

                # Inject the current relation
                tasks.append(self._inject_relation(ORM_Injectable, data, session, dependencies))

        # Run all tasks concurrently
        await gather(*tasks)
        await session.commit()

    async def _inject_relation(self, relation: Injectable, data, session: AsyncSession, dependencies):
        """
        Inject a single relation, waiting for dependencies to complete.
        :param relation: The model class to process.
        :param data: Parsed data object.
        :param session: Database session.
        :param dependencies: List of dependent table names.
        """
        tasks = []
        for dep in dependencies:
            tasks.append(self._get_event(dep).wait())
            ## await self._get_event(dep).wait()  # Wait for dependencies to complete
        await gather(*tasks)

        try:
            # Process the current relation
            await relation.process(data, session)
            await session.flush()  # Flush after processing
        except Exception as e:
            await session.rollback()
            print(f"Error processing {relation.__tablename__}: {e}")
        finally:
            # Signal that this relation is complete
            name = f"{relation.__tableschema__}.{relation.__tablename__}"
            self._get_event(name).set()
