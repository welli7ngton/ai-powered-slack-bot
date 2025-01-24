FROM python:3.10-alpine3.21

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry

RUN poetry install --no-root

COPY ./backend ./backend

ENV PYTHONUNBUFFERED=1

# Comando para iniciar o aplicativo
CMD ["poetry", "run", "python", "backend/app.py"]
