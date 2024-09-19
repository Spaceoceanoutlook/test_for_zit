FROM python:3.12
WORKDIR /app
COPY pyproject.toml poetry.lock* ./
RUN pip install poetry
RUN poetry install --no-root --no-dev
COPY ./app ./app
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
