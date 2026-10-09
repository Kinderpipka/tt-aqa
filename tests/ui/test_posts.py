import json

import allure
import pytest
from playwright.sync_api import Page, Route


@allure.epic("UI tests")
@allure.feature("Posts Page")
class TestPostsPage:
    @allure.title("Мокинг API ответа")
    @allure.description("Перехватываем запрос к API и подменяем ответ")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_mock_api_response(self, page: Page) -> None:
        mock_posts = [
            {"userId": 1, "id": 1, "title": "Mocked post 1", "body": "Mocked body 1"},
            {"userId": 2, "id": 2, "title": "Mocked post 2", "body": "Mocked body 2"},
        ]

        with allure.step("Настраиваем мокинг для /posts"):
            page.route(
                "**/posts",
                lambda route: route.fulfill(status=200, content_type="application/json", body=json.dumps(mock_posts)),
            )

        with allure.step("Открываем страницу /posts"):
            page.goto("https://jsonplaceholder.typicode.com/posts")

        with allure.step("Проверка, что получены моковые данные"):
            content = page.locator("pre").text_content()
            assert "Mocked post 1" in content
            assert "Mocked post 2" in content

    @allure.title("Перехват и проверка запросов")
    @allure.description("Проверяем, какие запросы уходят со страницы")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_capture_requests(self, page: Page) -> None:

        captured_requests = []

        with allure.step("Настраиваем перехват запросов"):

            def handle_request(route: Route) -> None:
                captured_requests.append(route.request.url)
                route.continue_()

            page.route("**/*", handle_request)

        with allure.step("Открываем главную страницу"):
            page.goto("https://jsonplaceholder.typicode.com")

        with allure.step("Проверяем, что были запросы к API"):
            api_requests = [url for url in captured_requests if "jsonplaceholder" in url]
            assert len(api_requests) > 0
            allure.attach(
                "\n".join(api_requests), name="Captured API Requests", attachment_type=allure.attachment_type.TEXT
            )

    @allure.title("Работа с медленным API (эмуляция)")
    @allure.description("Эмулируем задержку ответа API")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_slow_api_response(self, page: Page) -> None:

        mock_post = {"userId": 1, "id": 1, "title": "Slow Post", "body": "Slow body"}

        with allure.step("Настраиваем мокинг с задержкой 2 секунды"):

            def slow_response(route: Route) -> None:
                import time

                time.sleep(2)
                route.fulfill(status=200, content_type="application/json", body=json.dumps(mock_post))

            page.route("**/posts/1", slow_response)

        with allure.step("Запрашиваем пост и замеряем время"):
            import time

            start = time.time()
            page.goto("https://jsonplaceholder.typicode.com/posts/1")
            elapsed = time.time() - start

        with allure.step("Проверяем, что запрос занял больше 2 секунд"):
            assert elapsed >= 2.0
            allure.attach(
                f"Request took {elapsed:.2f} seconds", name="Response Time", attachment_type=allure.attachment_type.TEXT
            )
