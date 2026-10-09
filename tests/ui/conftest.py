import pytest
from playwright.sync_api import Page

from src.pages.home_page import HomePage


@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)
