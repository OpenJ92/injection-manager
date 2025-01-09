from collections import defaultdict

from injection_manager.typeclass.Injectable import Injectable
from injection_manager.typeclass.Session import AsyncSession

class InjectionManager():
    def __init__(self, base):
        """
        Initialize the InjectionManager.
        :param metadata: SQLAlchemy metadata (Base.metadata).
        """
        self.base = base
        self.metadata = base.metadata
        ## self.sorted_relations = self._topological_sort()


    async def inject(self, replay, session: AsyncSession):
        """
        Perform the injection process for a replay.
        :param replay: Parsed replay object to inject.
        :param session: Database session supporting flush, commit and rollback:
        """
        try:
            for relation in self.metadata.sorted_tables:
                name = f"{relation.schema}.{relation.name}"
                relation_cls = self.base.injectable.get(name)
                if relation_cls:
                    print(f"Inject relation - {name}")
                    await relation_cls.process(replay, session)
                    await session.flush()  # Flush after each relation
            await session.commit()

        except Exception as e:
            await session.rollback()
            import traceback
            print(f"Unexpected error: {e} in {name}")
            print(traceback.format_exc())
            # Gracefully handle all other exceptions



## ## Consider Supplying a "Base" at each level of the starcraft_data_orm via __init__.py file
## class InjectionManagerFactory():
##     def __init__(self):
##         pass
## 
##     @classmethod
##     def WAREHOUSE(cls):
##         return InjectionManager(WareshouseBase)
## 
##     @classmethod
##     def ANALYTICS(cls):
##         return InjectionManager(AnalyticsBase)
## 
##     @classmethod
##     def MACHINE_LEARNING(cls):
##         return InjectionManager(MachineLearningBase)

