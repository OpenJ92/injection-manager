from typing import Protocol
from collections import defaultdict

class Injectable(Protocol):
    @classmethod
    @property
    def __tableschema__(cls):
        """Return the schema name. Must be implemented by subclasses."""
        pass

    @classmethod
    def sync_process(cls, replay, session):
        """Must be implemented by subclasses."""
        pass
