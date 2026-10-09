from playwright.sync_api import Page

from src.pages.base_page import BasePage


class PostsPage(BasePage):
    URL = "https://jsonplaceholder.typicode.com/posts"

    def __init__(self, page: Page):
        super().__init__(page)
        self.post_item = page.locator("pre")
        self.first_post = page.locator("pre").first

    def open(self, url: str | None = None) -> None:
        target_url = url if url is not None else self.URL
        self.page.goto(target_url)

    def get_posts_count(self) -> int:
        return int(self.post_item.count())

    def get_first_post_text(self) -> str:
        return str(self.first_post.text_content())
