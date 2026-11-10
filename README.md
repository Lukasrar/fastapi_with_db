# FastAPI with Database

A learning project that combines a FastAPI REST API with a browser-based
to-do application. Users can register and log in, manage their own to-do
items, and update account information. The application uses SQLAlchemy with
SQLite, JWT bearer tokens, and server-rendered Jinja2 templates.

## Features

- Register users and authenticate with a username and password.
- Hash passwords with bcrypt and issue JWT access tokens that expire after
  20 minutes.
- Manage to-do items through both JSON endpoints and HTML pages.
- Restrict to-do operations to the authenticated user; admins can list and
  delete any to-do item.
- View user profile information, change a password, and update a phone number.
- Serve interactive API documentation, including Swagger UI and ReDoc.
- Run a health check at `/health-check`.

## Technologies

- **Python**, **FastAPI**, **Pydantic**, and **SQLAlchemy**
- **SQLite** for local relational data storage
- **Jinja2** templates with static CSS and JavaScript for the web interface
- **OAuth2 password flow** and **JWT** access tokens, implemented with
  `python-jose`
- **Passlib** and **bcrypt** for password hashing
- **Alembic** for database migrations
- **Uvicorn** as the ASGI server
- **pytest** for automated tests

## Requirements

- Python 3.9 or newer
- `pip`

## Installation

Clone the repository, create a virtual environment, and install the listed
runtime dependencies:

```bash
git clone https://github.com/Lukasrar/fastapi_with_db.git
cd fastapi_with_db
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The application also uses Jinja2 to render its HTML pages; it is not currently
listed in `requirements.txt`, so install it separately:

```bash
python -m pip install Jinja2
```

On Windows PowerShell, activate the virtual environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the application

Start the development server from the repository root:

```bash
uvicorn main:app --reload
```

The application is available at <http://127.0.0.1:8000>.

| Resource | URL |
| --- | --- |
| Web application | <http://127.0.0.1:8000/> |
| Swagger UI | <http://127.0.0.1:8000/docs> |
| ReDoc | <http://127.0.0.1:8000/redoc> |
| OpenAPI schema | <http://127.0.0.1:8000/openapi.json> |
| Health check | <http://127.0.0.1:8000/health-check> |

The root URL redirects to `/todos/todo-page`. The SQLite database URL is
configured in `database.py` and currently points to `todosapp.db` in the
working directory. SQLAlchemy creates missing tables when the application
starts.

## Web pages

The browser interface includes registration and login pages, a page listing
the current user's to-do items, and forms for adding and editing items.
After login, the browser stores the access token in a cookie and sends it with
requests to protected API endpoints.

| Page | URL |
| --- | --- |
| Login | `/auth/login-page` |
| Registration | `/auth/register-page` |
| To-do list | `/todos/todo-page` |
| Add a to-do item | `/todos/add-todo-page` |
| Edit a to-do item | `/todos/edit-todo-page/{todo_id}` |

Visiting a protected page without a valid token redirects to the login page.

## Authentication

### Register a user

Send a JSON request to `POST /auth/`:

```bash
curl -X POST http://127.0.0.1:8000/auth/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Example",
    "password": "change-this-password",
    "role": "user",
    "phone_number": "555-0100"
  }'
```

The request requires `username`, `email`, `first_name`, `last_name`,
`password`, `role`, and `phone_number`.

### Log in

Send the username and password as form fields to `POST /auth/token`:

```bash
curl -X POST http://127.0.0.1:8000/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "username=alice" \
  --data-urlencode "password=change-this-password"
```

The response contains an `access_token` and `token_type` (`bearer`). Include
the token in the `Authorization` header when calling protected API endpoints:

```bash
curl http://127.0.0.1:8000/todos/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## API endpoints

The to-do API only returns or modifies items owned by the authenticated user.
Attempting to access another user's item returns `404`.

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Redirect to the to-do web page |
| `GET` | `/health-check` | Check application health |
| `POST` | `/auth/` | Register a user |
| `POST` | `/auth/token` | Authenticate and obtain a bearer token |
| `GET` | `/todos/` | List the authenticated user's items |
| `GET` | `/todos/todo/{todo_id}` | Get one of the authenticated user's items |
| `POST` | `/todos/todo` | Create a to-do item |
| `PUT` | `/todos/todo/{todo_id}` | Update one of the authenticated user's items |
| `DELETE` | `/todos/todo/{todo_id}` | Delete one of the authenticated user's items |
| `GET` | `/admin/todo` | List all to-do items (admin only) |
| `DELETE` | `/admin/todo/{todo_id}` | Delete any to-do item (admin only) |
| `GET` | `/user/get-user` | Get the authenticated user's profile |
| `PUT` | `/user/change-password` | Change the authenticated user's password |
| `PUT` | `/user/change-phone-number/{phone_number}` | Update the authenticated user's phone number |

A to-do request body has this shape:

```json
{
  "title": "Read the documentation",
  "description": "Review the API endpoints",
  "priority": 2,
  "complete": false
}
```

Validation requires a title of at least 3 characters, a description between 3
and 100 characters, a priority from 1 through 6, and a boolean `complete`
value.

## Database migrations

The repository includes an Alembic configuration and a migration that adds the
`phone_number` column to the users table. Application startup also calls
SQLAlchemy `create_all`, which creates missing tables but does not update
existing tables when models change. Review the current database schema and
Alembic revision before applying migrations to an existing database; the
included migration is not a general schema migration for every database state.

Install Alembic if you need to use the migration tooling:

```bash
python -m pip install alembic
```

## Tests

The tests use pytest, pytest-asyncio, and FastAPI's TestClient (which requires
HTTPX). These packages are not currently listed in `requirements.txt`.
Install them and run the test suite with:

```bash
python -m pip install pytest pytest-asyncio httpx
python -m pytest
```

## Project layout

```text
.
├── main.py              # FastAPI app, static files, and router registration
├── database.py          # SQLite URL, SQLAlchemy engine, and session factory
├── models.py            # User and to-do database models
├── requirements.txt     # Listed runtime dependencies
├── routers/
│   ├── auth.py          # Registration, login, and token validation
│   ├── todos.py         # To-do API and HTML page routes
│   ├── admin.py         # Admin-only to-do endpoints
│   └── user.py          # Profile and account-management endpoints
├── templates/           # Jinja2 pages for authentication and to-dos
├── static/              # CSS and JavaScript assets
├── utils/hash.py        # Password hashing and JWT configuration
├── alembic/             # Database migration environment and revisions
└── test/                # pytest tests and shared fixtures
```

## Security note

This project is intended as a learning example, not for production use. The
JWT signing key is hard-coded, and registration accepts a role from the
request body, so a client can choose its own role. Replace the signing key
with secure configuration and enforce role assignment on the server before
deployment.
