from typing import Protocol

class Injectable(Protocol):
    @classmethod
    @property
    def __tableschema__(cls):
        """Return the schema name. Must be implemented by subclasses."""
        pass

    @classmethod
    def process(cls, replay, session):
        """Must be implemented by subclasses."""
        pass
