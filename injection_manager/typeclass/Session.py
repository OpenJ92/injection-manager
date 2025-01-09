from typing import Protocol

class AsyncSession(Protocol):
    async def flush(self):
        """ Flush the current state of the session to the database. """
        pass

    async def commit(self):
        """ Commit the current transaction to the database. """
        pass

    async def rollback(self):
        """ rollback current transaction. """
        pass

    def add(self, element):
        """ Add one instance to the session. """
        pass

    def add_all(self, elements):
        """ Add multiple instances to the session. """
        pass
