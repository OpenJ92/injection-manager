from typing import Protocol
from injection_manager.typeclass.Session import AsyncSession

class Injectable(Protocol):
    @classmethod
    @property
    def __tableschema__(cls):
        """Return the schema name. Must be implemented by subclasses."""
        pass

    @classmethod
    async def process(cls, replay, session: AsyncSession):
        """
        Process the provided data and add it to the session.

        This method should be implemented by subclasses to handle the logic
        for processing the given replay data and adding the resulting
        objects to the session. Note that flushing and committing the session
        are managed by the InjectionManager and should not be handled here.

        Parameters:
        - replay: The replay data to process.
        - session: The database session to which processed objects should be added.
        """
        pass
