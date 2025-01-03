# Injection Manager
Injection Manager is a lightweight and async-enabled data injection framework for Python. It is designed to work seamlessly with SQLAlchemy and makes managing data pipelines simpler and more efficient.

### Features
- Works with both synchronous and asynchronous SQLAlchemy sessions.
- Easily extensible through custom injectable models.
- Designed with testing in mind, supporting mock data and test utilities.
- Modular and scalable for complex workflows.

### Installation
To install the package, run:

```code
pip install injection-manager
```

### Usage
Define an Injectable Model
Create a custom model that inherits from the Injectable class and implements the process method:

```python
Copy code
from injection_manager import Injectable

class MyModel(Injectable):
    @staticmethod
    async def process(data, session):
        # Process data and add it to the session
        session.add(data)
```

### Inject Data
Use the InjectionManager to inject data into the database:

```python
Copy code
from injection_manager import InjectionManager
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine("postgresql+asyncpg://user:password@host/dbname")
manager = InjectionManager(sessionmaker=engine)
```

### Inject data
```python 
await manager.inject(MyModel, data)
```

### Testing
You can mock sessions and use test utilities to validate your process methods.

Example Test
```python
Copy code
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_process():
    mock_session = AsyncMock()
    data = {"id": 1, "name": "Test"}
    await MyModel.process(data, mock_session)
    mock_session.add.assert_called_once_with(data)
```

License
This project is licensed under the MIT License.

