# Course Task API

A Flask REST API for managing users, lecturers, courses, and course tasks. The application uses PostgreSQL for persistence, SQLAlchemy for data access, Alembic/Flask-Migrate for schema migrations, JWT for authentication, and Flasgger for API documentation.

## Current Features

- User authentication with access and refresh tokens
- CRUD-style creation and lookup flows for users, lecturers, courses, and course tasks
- Filtering endpoints for lecturers, courses, and course tasks
- Request tracing and centralized exception handling
- Swagger UI generated from the route documentation

## Requirements

- Python 3.11 or newer
- Docker and Docker Compose
- PostgreSQL (Docker Compose provides a local instance)

## Getting Started

1. Create and activate a virtual environment:

	```bash
	python -m venv .venv
	source .venv/bin/activate
	```

2. Install the dependencies:

	```bash
	pip install -r requirements.txt
	```

3. Start PostgreSQL:

	```bash
	docker compose up -d lumidb
	```

4. Create a `.env` file in the project root. These values match the local database configured in `docker-compose.yml`:

	```dotenv
	SECRET_KEY=replace-with-a-long-random-value
	DATABASE_URL=postgresql+psycopg://DBUSER:DBPASSWORD!@localhost:5432/DBNAME
	APP_ENVIRONMENT=development
	```

	Keep `.env` out of version control and use different credentials outside local development.

5. Apply the database migrations:

	```bash
	flask --app app.main db upgrade
	```

6. Start the API:

	```bash
	flask --app app.main run --debug
	```

The API is available at `http://127.0.0.1:5000`.

## API Documentation

Open the Swagger UI at `http://127.0.0.1:5000/apidocs/` while the application is running. Protected endpoints require a bearer token returned by `POST /authentications/login`.

## Main Endpoints

| Area | Endpoints |
| --- | --- |
| Authentication | `POST /authentications/login`, `POST /authentications/refresh`, `POST /authentications/logout` |
| Users | `POST /users/`, `GET /users/<id>`, `GET /users/search` |
| Lecturers | `POST /lecturers/`, `GET /lecturers/<id>`, `GET /lecturers/search` |
| Courses | `POST /courses/`, `GET /courses/<id>`, `GET /courses/search` |
| Course tasks | `POST /course_tasks/`, `GET /course_tasks/<id>`, `GET /course_tasks/search` |

UUID values are used for entity identifiers. Request and response payloads are validated with Pydantic DTOs and returned through the API response wrapper.

## Database Commands

Create a migration after changing a model:

```bash
flask --app app.main db migrate -m "describe the schema change"
flask --app app.main db upgrade
```

Stop the local database with:

```bash
docker compose down
```

## Next Features

### Alerts with custom webhooks

Add an alert service that can notify external channels when important events occur, such as a task becoming overdue or an AI generation failing. The first integrations are planned for:

- Discord webhook URLs
- Telegram bot tokens and chat IDs

Planned configuration values:

```dotenv
DISCORD_WEBHOOK_URL=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
ALERTS_ENABLED=false
```

Webhook delivery should be handled asynchronously, use timeouts and retries, and never expose webhook secrets in logs or API responses.

### AI-generated task results

Add an authenticated endpoint that generates a result or summary for an existing course task:

```text
GET /coursetask/<id>/generate
```

The endpoint is a planned feature and is not available in the current application. It should verify that the task exists and that the caller has access to it, send the task context to the configured AI provider, persist the generated result, and return the generated content with its status and timestamp.

Planned configuration values:

```dotenv
AI_PROVIDER=
AI_API_KEY=
AI_MODEL=
```

The current resource prefix is `/course_tasks`; the generation route should either follow that existing convention as `/course_tasks/<id>/generate` or provide a documented compatibility alias for the requested `/coursetask/<id>/generate` path.

## Project Structure

```text
app/
  routes/          HTTP endpoints and request validation
  services/        application logic
  repositories/    database access
  models/          SQLAlchemy models
  schemas/         Pydantic DTOs
  middlewares/     request tracing and exception handling
  cores/           application configuration and extensions
migrations/        Alembic migration history
database/          local PostgreSQL data volume
```
