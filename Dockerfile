# Используем официальный образ Python
FROM python:3.10-slim
# Устанавливаем рабочую директорию
WORKDIR /app
# Копируем файлы конфигурации Poetry
COPY pyproject.toml poetry.lock* ./
# Устанавливаем Poetry
RUN pip install poetry
# Устанавливаем зависимости
RUN poetry install --no-root --no-dev
# Копируем остальной код приложения
COPY ./app ./app
# Указываем команду для запуска приложения
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
