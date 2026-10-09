
FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

RUN uv run playwright install chromium --with-deps

COPY . .

CMD ["uv", "run", "pytest", "tests/", "-v", "--alluredir=allure-results --clean-alluredir"]