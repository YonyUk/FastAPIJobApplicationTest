# <center>FastAPI Job Application Test</center>

## Description

This is an app to manage **Posts** published by **Users**. Each post can be labeled with a set of **Tags**, and have many **Comments**. Tags have descriptions and every comment have an author, so when we ask for a post, we gets with it its tags and comments, where tags shows its description and comments shows its author. A user can only delete or modify his own posts and comments, and only a user can delete or modify themselves

## Technical dependencies

 - Python 3.11 or higher
 - postgresql 15 or higher
 - Docker (Optional if you want to deploy the app with it)

## Deploying

> ### Local
 - `1`: Install ***PostgresQL***

 - `2`: Create a virtual environment:

```bash
# windows
python -m venv "name_of_your_environment"

# linux
python3 -m venv "name_of_your_environment"
```

 - `3`: Copy all the content of this project inside the new folder have been created

 - `4`: Create a file named ***.env*** (no extension) with this content:

```properties
# Settings for the app
DB_ENGINE=postgresql
DB_USER=your_user
DB_HOST=localhost
DB_PASSWORD=your_password
DB_PORT=your_port
DB_NAME=your_db
API_GLOBAL_PREFIX=/api/v1
VERSION=1.0.0
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRES_MINUTES=5 # the time you want
ALEMBIC_CONFIG_FILE=alembic.ini
SQLALCHEMY_POOL_SIZE=85 # the pool size for asynchronous requests to database
SQLALCHEMY_MAX_OVERFLOW=10
SQLALCHEMY_POOL_TIMEOUT=60
MIN_USERNAME_LENGTH=4 # your decision
MAX_USERNAME_LENGTH=50 # your decision
MIN_USER_PASSWORD_LENGTH=8 # your decision
MAX_USER_PASSWORD_LENGTH=30 # your decision
MIN_POST_TITLE_LENGTH=1 # your decision
MAX_POST_TITLE_LENGTH=100 # your decision
PAGES_SIZE = 100 # your decision
```

 - `5`: Open the ***alembic.ini*** file:

```properties
# replace this line by its respective values
sqlalchemy.url = postgresql+asyncpg://your_user:your_password@localhost:your_port/your_db
```

 - `6`: Run this commands in a terminal opened in the root directory of this project:

```bash
pip install --no-cache-dir -r requirements.txt
``` 

 - `7`: Run this command in a terminal opened in the root directory of this project:

```bash
# creates the migration
alembic revision --autogenerate -m "making migrations"

# creates all the database structure
alembic upgrade head
```

 - `8`: Execute the app in a terminal opened in the root directory of this project:

```bash
# dev mode with file reload
fastapi dev # or uvicorn main:app --host <address> --port <port> --reload

# or in deploy mode
fastapi run # or uvicorn main:app --host <address> --port <port>
```

 - `9`: Open your browser at http://localhost:8000/docs (if you don't use the "fastapi" command, you must replace 8000 by the selected port)

> ### Docker

 - `1` Clone this repository

 - `2`: Enter to project folder and create the file ***.env*** with the same content showed before

 - `3`: Open the file ***docker-compose.yml***:

```yml
# replace this lines with its respective values
environment:
      - POSTGRES_USER=your_user
      - POSTGRES_PASSWORD=your_password
      - POSTGRES_DB=your_db
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U your_user -d your_db"]
```

 - `4`: Build the images:

```bash
docker-compose up -d --build
```


- `5`: Open your browser in the respective address

