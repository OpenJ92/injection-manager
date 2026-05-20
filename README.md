# Injection Manager
Injection Manager is a lightweight, async-enabled data injection framework for
Python. It coordinates custom injectable classes against SQLAlchemy-style
metadata so parsed data can be written to related database tables in dependency
order.

### Features
- Works with asynchronous SQLAlchemy-style sessions.
- Processes injectable models in `Base.metadata.sorted_tables` order.
- Flushes after each injectable and commits once the full injection succeeds.
- Rolls back the session if an injectable raises an error.
- Exposes both sequential and event-based injection managers.

### Installation
To install the package, run:

```sh
pip install injection-manager
```

### Usage
Define an injectable model by implementing the `Injectable` protocol. The
manager handles flushing and committing, so injectable classes should only add
objects to the session.

```python
from injection_manager import Injectable

class MyModel(Injectable):
    __tableschema__ = "public"
    __tablename__ = "my_model"

    @classmethod
    async def process(cls, data, session):
        # Process data and add it to the session
        session.add(data)
```

Create an `InjectionManager` with a SQLAlchemy declarative base-like object. The
base must provide:

- `metadata.sorted_tables`, where each table has `schema` and `name`
- `injectable`, a dictionary keyed by `"schema.table"` and valued by injectable
  classes

Then pass parsed data and an async session to `inject`.

```python
from injection_manager import InjectionManager

manager = InjectionManager(WarehouseBase)
await manager.inject(replay, session)
```

`EventInjectionManager` is also available for dependency-aware concurrent
injection. It waits for foreign-key dependencies before processing dependent
relations.

### Testing
You can mock sessions to validate injectable `process` methods.

```python
import unittest
from unittest.mock import Mock

class MyModelTest(unittest.IsolatedAsyncioTestCase):
    async def test_process(self):
        mock_session = Mock()
        data = {"id": 1, "name": "Test"}

        await MyModel.process(data, mock_session)

        mock_session.add.assert_called_once_with(data)
```

### License
This project is licensed under the MIT License.
