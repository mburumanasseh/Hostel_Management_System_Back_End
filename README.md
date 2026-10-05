# Zabe Hostel Management System — Backend

Flask API for the Zabe Hostel Management System.

## Database

**PostgreSQL** (migrated from MySQL).

Connection is configured via environment variables (see `.env.example`):

| Variable      | Example          |
|---------------|------------------|
| `DB_USER`     | `postgres`       |
| `DB_PASSWORD` | `your_password`  |
| `DB_HOST`     | `localhost`      |
| `DB_PORT`     | `5432`           |
| `DB_NAME`     | `zabe_hostel_db` |

SQLAlchemy URI format: `postgresql+psycopg2://...`

## Setup

```bash
# 1. Install dependencies
pipenv install
# (this will resolve psycopg2-binary and update Pipfile.lock)

# 2. Copy env and fill in values
cp .env.example .env

# 3. Create the PostgreSQL database
createdb zabe_hostel_db   # or via psql / your host provider

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
