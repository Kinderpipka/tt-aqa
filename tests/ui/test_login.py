import allure
import pytest

from src.pages.home_page import HomePage


@allure.epic("UI tests")
@allure.feature("Home Login")
class TestHomePage:
    @allure.title("Открыть главную страницу")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_open_homepage(self, home_page: HomePage) -> None:
        with allure.step("Открываем главную страницу"):
            home_page.open()

        with allure.step("Проверяем заголовок"):
            assert home_page.get_title() == "JSONPlaceholder - Free Fake REST API"

        with allure.step("Проверка, что страница содержитт текст JSONPlaceholder"):
            assert home_page.contains_text("JSONPlaceholder")

    @allure.title("Проверить наличие ссылок на ресурсы")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_check_resource_links(self, home_page: HomePage) -> None:

        with allure.step("Открытие главной страницы"):
            home_page.open()

        with allure.step("Проверка наличия ссылки /posts"):
            assert home_page.is_posts_link_visible()

        with allure.step("Проверка наличия ссылки /comments"):
            assert home_page.is_comments_link_visible()

        with allure.step("Проверка наличия ссылки /users"):
            assert home_page.is_users_link_visible()
