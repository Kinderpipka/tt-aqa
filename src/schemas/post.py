from pydantic import BaseModel, Field


class Post(BaseModel):
    id: int = Field(description="Идентификатор")
    title: str = Field(min_length=1, description="Заголовок")
    body: str = Field(min_length=1, description="Описание")
    userId: int = Field(description="пользователь номер")


class PostCreate(BaseModel):
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)
    userId: int


class PostUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    userId: int | None = None
