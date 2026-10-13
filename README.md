# Zabe Hostel Management System — Backend

Flask API for the Zabe Hostel Management System.

## Database

**PostgreSQL** (migrated from MySQL).

Connection is configured via environment variables in a local `.env` file (gitignored):

| Variable      | Example                |
|---------------|------------------------|
| `DB_USER`     | `hostel_user`          |
| `DB_PASSWORD` | `your_password`        |
| `DB_HOST`     | `localhost`            |
| `DB_PORT`     | `5432`                 |
| `DB_NAME`     | `hostel_management_db` |
| `SECRET_KEY`  | long random string     |
| `JWT_SECRET_KEY` | long random string  |

SQLAlchemy URI format: `postgresql+psycopg2://...`

## Setup

```bash
# 1. Install dependencies
pipenv install

# 2. Create a local .env with the variables above

# 3. Create the PostgreSQL database (if needed)
#    via psql or createdb

# 4. Run migrations
export FLASK_APP=run.py
pipenv run flask db upgrade

# 5. Start the server
pipenv run python run.py
```

## Stack

- Flask + Flask-SQLAlchemy + Flask-Migrate
- Flask-JWT-Extended + Flask-Bcrypt
- Flask-Marshmallow
- PostgreSQL via `psycopg2-binary`
- Gunicorn (production)

## Modules

Auth, Students, Blocks, Rooms, Allocations, Maintenance, Payments, Hostel Fees.
