import allure
import pytest

from core.database import DatabaseManager


@allure.epic("Database Tests")
@allure.feature("Task Management")
class TestDatabase:
    @allure.title("Создать задачу в БД")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_create_task_in_db(self, db_manager: DatabaseManager) -> None:

        with allure.step("Создаём задачу"):
            task = db_manager.create_task(title="Test Task in DB", body="Test body", user_id=1)

        with allure.step("Проверяем, что задача создана"):
            assert task.id is not None
            assert task.title == "Test Task in DB"
            assert task.body == "Test body"
            assert task.user_id == 1

    @allure.title("Получить задачу по ID")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_get_task_by_id(self, db_manager: DatabaseManager) -> None:

        with allure.step("Создаём задачу"):
            task = db_manager.create_task(title="Task to retrieve", body="Body to retrieve", user_id=2)

        with allure.step("Получаем задачу по ID"):
            retrieved_task = db_manager.get_task_by_id(task.id)

        with allure.step("Проверяем данные"):
            assert retrieved_task is not None
            assert retrieved_task.id == task.id
            assert retrieved_task.title == "Task to retrieve"

    @allure.title("Получить все задачи")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_tasks(self, db_manager: DatabaseManager) -> None:

        with allure.step("Создаём несколько задач"):
            db_manager.create_task("Task 1", "Body 1", 1)
            db_manager.create_task("Task 2", "Body 2", 2)

        with allure.step("Получаем все задачи"):
            all_tasks = db_manager.get_all_tasks()

        with allure.step("Проверяем количество"):
            assert len(all_tasks) >= 2

    @allure.title("Удалить задачу")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_task(self, db_manager: DatabaseManager) -> None:

        with allure.step("Создаём задачу"):
            task = db_manager.create_task("Task to delete", "Body", 1)

        with allure.step("Удаляем задачу"):
            result = db_manager.delete_task(task.id)

        with allure.step("Проверяем удаление"):
            assert result is True
            assert db_manager.get_task_by_id(task.id) is None
