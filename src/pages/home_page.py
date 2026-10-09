from playwright.sync_api import Page, expect

from src.pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, page: Page):
        super().__init__(page)
        self.posts_link = page.locator("a[href='/posts']").first
        self.comments_link = page.locator("a[href='/comments']").first
        self.users_link = page.locator("a[href='/users']").first
        self.body = page.locator("body")

    def open(self, url: str | None = None) -> None:
        target_url = url if url is not None else self.URL
        self.page.goto(target_url)

    def get_title(self) -> str:
        return str(self.page.title())

    def is_posts_link_visible(self) -> bool:
        expect(self.posts_link).to_be_visible()
        return True

    def is_comments_link_visible(self) -> bool:
        expect(self.comments_link).to_be_visible()
        return True

    def is_users_link_visible(self) -> bool:
        expect(self.users_link).to_be_visible()
        return True

    def contains_text(self, text: str) -> bool:
        expect(self.body).to_contain_text(text)
        return True
