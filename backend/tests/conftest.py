import pytest
import asyncio
from typing import Generator

@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """
    Create an instance of the default event loop for the test session.
    This ensures that the same loop is used for all tests, avoiding
    SQLAlchemy InterfaceError with global async engines.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
