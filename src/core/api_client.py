from typing import Any

from httpx import Client

from schemas.post import Post, PostCreate


class TaskTrackerAPIClient:
    def __init__(self, base_url: str = "https://jsonplaceholder.typicode.com"):
        self.client = Client(base_url=base_url, timeout=30.0)

    def close(self) -> None:
        self.client.close()

    def get_posts(self) -> list[Post]:
        response = self.client.get("/posts")
        response.raise_for_status()
        return [Post(**post) for post in response.json()]

    def get_post(self, post_id: int) -> Post:
        response = self.client.get(f"/posts/{post_id}")
        response.raise_for_status()
        return Post(**response.json())

    def create_post(self, data: PostCreate) -> Any:

        response = self.client.post("/posts", json=data.model_dump())

        return response.json() if response.status_code == 201 else None

    def update_post(self, post_id: int, data: dict[str, Any]) -> Any:

        response = self.client.put(f"/posts/{post_id}", json=data)
        return response.json() if response.status_code == 200 else None

    def delete_post(self, post_id: int) -> int:

        response = self.client.delete(f"/posts/{post_id}")
        return int(response.status_code)
