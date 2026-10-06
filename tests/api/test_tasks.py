import allure
import pytest
from pydantic import ValidationError

from core.api_client import TaskTrackerAPIClient
from schemas.post import Post, PostCreate


@allure.epic("Api tests")
@allure.feature("Posts")
class TestPostsAPI:
    @allure.title("Получить все задачи")
    @allure.description("Прверяем, что возвращаеться список задач")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_all_posts(self, api_client: TaskTrackerAPIClient) -> None:
        with allure.step("Отправка запроса get на /posts"):
            posts = api_client.get_posts()

        with allure.step("Проверка что список не пуст"):
            assert len(posts) > 0
        with allure.step("Проверка структуры первой задачи"):
            assert isinstance(posts[0], Post)
            assert posts[0].id > 0
            assert len(posts[0].title) > 0

    @allure.title("Получить 1 задачу")
    @allure.description("Проверяем получение задачи по идентификатору")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_get_single_post(self, api_client: TaskTrackerAPIClient, post_id: int) -> None:
        with allure.step(f"Отправляем запрос get на /posts/{post_id}"):
            post = api_client.get_post(post_id)
        with allure.step("Проверяем ID задачи"):
            assert post.id == post_id
        with allure.step("Проверяем наличия обязательных полей"):
            assert len(post.title) > 0
            assert len(post.body) > 0
            assert post.userId > 0

    @allure.title("Создания задачи")
    @allure.description("Проверка создания задачи")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_create_post(self, api_client: TaskTrackerAPIClient) -> None:

        new_post_data = PostCreate(title="New Task via Pydantic", body="Description via Pydantic", userId=1)

        with allure.step("Подготовка данных для создания"):
            allure.attach(
                new_post_data.model_dump_json(indent=2),
                name="body",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Отправка запроса post на /posts"):
            result = api_client.create_post(new_post_data)

        with allure.step("Проверка результата"):
            if result is not None:
                allure.attach(
                    str(result),
                    name="body",
                    attachment_type=allure.attachment_type.JSON,
                )
                assert result["title"] == new_post_data.title
                assert result["body"] == new_post_data.body
                assert result["userId"] == new_post_data.userId

    @allure.title("Обновить задачу")
    @allure.description("Проверка обнавления задачи")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_update_post(self, api_client: TaskTrackerAPIClient, post_id: int) -> None:

        update_data = {"title": "Updated Task"}

        with allure.step(f"Отправляем запрос PUT на /posts/{post_id}"):
            result = api_client.update_post(post_id, update_data)

        with allure.step("Проверяем результат"):
            if result is not None:
                assert result["title"] == "Updated Task"

    @allure.title("Удалить задачу")
    @allure.description("Проверка удаления задачи")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.api
    def test_delete_post(self, api_client: TaskTrackerAPIClient, post_id: int) -> None:

        with allure.step(f"Отправляем запрос DELETE на /posts/{post_id}"):
            status_code = api_client.delete_post(post_id)

        with allure.step("Проверка статус кодов"):
            assert status_code in [200, 404]

    @allure.title("Валидация Pydantic модели")
    @allure.description("Проверка что ловятся ошибки структуры")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    def test_post_validation_fails_on_missing_field(self) -> None:

        invalid_data = {"id": 1, "title": "Test"}

        with allure.step("Попытка создать Post без обязательных полей"):
            with pytest.raises(ValidationError) as exc_info:
                Post(**invalid_data)

        with allure.step("Проверка что обишка содержит недостоющие поля"):
            assert "body" in str(exc_info.value)
            assert "userId" in str(exc_info.value)
