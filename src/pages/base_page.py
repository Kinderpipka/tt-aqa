from playwright.sync_api import Locator, Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str) -> None:
        self.page.goto(url)

    def get_title(self) -> str:
        return str(self.page.title())

    def is_visible(self, locator: Locator) -> bool:
        expect(locator).to_be_visible()
        return True
