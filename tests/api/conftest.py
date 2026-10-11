from typing import Any, Generator

import pytest

from core.database import DatabaseManager
from src.core.api_client import TaskTrackerAPIClient


@pytest.fixture(scope="session")
def api_client() -> Generator[TaskTrackerAPIClient, None, None]:
    client = TaskTrackerAPIClient()
    yield client
    client.close()


@pytest.fixture
def task_data() -> dict[str, Any]:
    return {"title": "Test Task", "body": "Description for test", "userId": 1}


@pytest.fixture(scope="module")
def post_id() -> int:
    return 1


@pytest.fixture(scope="session")
def db_manager() -> Generator[DatabaseManager, None, None]:

    manager = DatabaseManager("sqlite:///test_tasks.db")
    yield manager
    # Очищаем БД после всех тестов
    manager.clear_all_tasks()


@pytest.fixture(scope="function")
def db_session(db_manager: DatabaseManager) -> Generator[DatabaseManager, None, None]:

    session = db_manager.get_session()
    yield session
    session.close()
