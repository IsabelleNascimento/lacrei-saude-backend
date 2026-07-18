FROM python:3.13-slim

WORKDIR /code

RUN apt-get update && apt-get install -y libpq-dev gcc

RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi --no-plugins


COPY . .

EXPOSE 8000

CMD ["python", "src/manage.py", "runserver", "0.0.0.0:8000"]