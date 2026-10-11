# 🧪 TT-AQA  Task Tracker Automation

Автоматизированное тестирование API и UI для Task Tracker (аналог Jira/Linear). 

## 🚀 Стек технологий

### Основные инструменты
- **Python 3.12** - язык программирования
- **Pytest** - фреймворк для тестирования
- **httpx** - HTTP - клиент для API тестов
- **Playwright** - автоматизация браузера для UI тестов
- **Pydantic** - валидация данных и схем
- **Allure** - генерация отчётов о тестировании

### Инфраструктура и качество кода
- **uv** - быстрый менеджер зависимостей
- **Ruff** - линтер и форматтер кода
- **mypy** - статическая проверка типов
- **pre-commit** - автоматические проверки перед коммитом
- **Docker** - контейнеризация тестового окружения
- **GitHub Actions** - CI/CD пайплайн

### Тестовые данные
- **Faker** - генерация уникальных тестовых данных
- **SQLAlchemy** - работа с базой данных


##  Установка и запуск

### Предварительные требования
- Python 3.12+
- uv (менеджер зависимостей)
- Allure CLI (для генерации отчётов)

### Шаги установки

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/Kinderpipka/tt-aqa.git
cd tt-aqa
uv sync
uv run playwright install chromium
uv run pre-commit install
uv run pytest

Параллельный запуск (ускорение в 2-4 раза):
uv run pytest -n auto

С генерацией Allure отчёта:
uv run pytest --alluredir=allure-results
allure generate allure-results -o allure-report --clean
allure open allure-report

Docker запуск
docker compose build
docker compose up
```
## Архитектура
### API тестирование
- API Client - инкапсулирует HTTP-запросы (GET, POST, PUT, DELETE)
- Pydantic Models - строгая валидация ответов API
- Faker - генерация уникальных данных для каждого теста
### UI тестирование
- Page Object Pattern - разделение локаторов и тестовой логики
- Base Page - базовый класс с общими методами
- Мокинг API - перехват и подмена ответов для стабильности
- Auto-waiting - встроенные ожидания Playwright
### Инфраструктура
- CI/CD - автоматический запуск при каждом push/PR
- Allure Reports - детальные отчёты с шагами и аттачментами
- Parallel Execution - ускорение прогона через pytest-xdist

## 🔧 Качество кода
### Проект использует строгие стандарты качества:
- Ruff - автоматическое форматирование и линтинг
- mypy - проверка типов (strict mode)
- pre-commit - проверки перед каждым коммитом
```bash
# Запустить линтеры вручную
uv run ruff check .
uv run ruff format .
uv run mypy .

# Запустить pre-commit на всех файлах
uv run pre-commit run --all-files
```
## 🚀 CI/CD
### Проект настроен с GitHub Actions:
- Автоматический запуск при push в main/master
- Запуск при создании Pull Request
- Параллельное выполнение тестов
- Сохранение Allure результатов как артефактов
- Установка зависимостей через uv с кешированием

## 📝 Используемые API
### Для тестирования используется JSONPlaceholder  бесплатный мок-API:
- Документация: https://jsonplaceholder.typicode.com/
- Эндпоинты: /posts, /comments, /users, /todos