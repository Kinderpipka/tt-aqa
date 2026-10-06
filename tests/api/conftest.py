from typing import Any, Generator

import pytest

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
