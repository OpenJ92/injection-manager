from typing import Protocol
from collections import defaultdict

class AsyncInjectable(Protocol):
    @classmethod
    @property
    def __tableschema__(cls):
        """Return the schema name. Must be implemented by subclasses."""
        pass

    @classmethod
    async def async_process(cls, replay, session):
        """Must be implemented by subclasses."""
        pass
