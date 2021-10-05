# Connecting to PostgreSQL database with asyncpg

## Requirements
1. [Python 3.7+](https://www.python.org/downloads/)
2. [Visual Code](https://code.visualstudio.com/download)
3. Docker

## Creating virtual environment and installing dependencies
1. Create a folder for this application and then open this folder in the terminal. 
2. Create a virtual environment with **`python -m venv <name>`** .
3. Activate the virtual environment with: **`<name>\Scripts\activate`**.
4. Create a **`requirements.txt`** file with the following libraries:

    ```
    fastapi==0.68.1
    asyncio==3.4.3
    asyncpg==0.24.0
    uvicorn==0.15.0
    ```
5. Install requirements.txt with **`pip install -r requirements.txt`**

## Creating PostgreSQL database
1. Create a **`docker-compose.yml`** file with the following content:

```yaml
version: '3.8'

services:
  postgresql:
    image: postgres:10-stretch
    container_name: pg-docker
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=username
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=db_sample
    volumes:
      - ./postgres.conf:/etc/postgresql/postgresql.conf
    command: postgres -c config_file=/etc/postgresql/postgresql.conf
    restart: always

  pgadmin:
    image: dpage/pgadmin4:5.7
    container_name: pg-admin
    ports:
      - "8085:8000"
    environment:
      - PGADMIN_DEFAULT_EMAIL=username@contoso.com
      - PGADMIN_DEFAULT_PASSWORD=password
```

In this yaml file, you are creating two services, postgresql database with user,password and db name and pgadmin (web client) to access the local db.


2. Create a new file **`postgres.conf`** with this content:

```log
listen_addresses = '*'
port = 5432
max_connections = 100
```
3. Run **`docker-compose up`** to run the two containers.
4. Browse to `http://localhost:8085/`, login with PGADMIN_DEFAULT_EMAIL and PGADMIN_DEFAULT_PASSWORD.
5. Create a Server with the following values:
- Host: pg-docker
- Username: with POSTGRES_USER value
- Password: with POSTGRES_PASSWORD value
6. Once you connect to the server, you can see db_sample already created.

## Create a FastAPI app
1. In the same terminal type **`code .`** to open the current directory in Visual Code.
2. In Visual Code, right click on left panel and select `New File`, change the name of the file to `app.py`.
3. Copy the following code in `app.py`:

```python
from fastapi import FastAPI
import asyncpg, asyncio, json, uvicorn

app = FastAPI()

async def getUsers():
    conn = await asyncpg.connect(user='username',password='password',
                                database='db_sample', host='localhost')

    await conn.execute('''
        DROP TABLE IF EXISTS Users 
    ''')

    await conn.execute('''
        CREATE TABLE Users(id serial PRIMARY KEY, 
                name VARCHAR(50) NOT NULL, 
                lastname VARCHAR(50) NOT NULL)
    ''')

    await conn.execute('''
        INSERT INTO Users (name, lastname)
        VALUES($1, $2)''', 'Name', 'LastName')

    records = await conn.fetch('SELECT * FROM Users')
    values = [dict(record) for record in records]
    result = json.dumps(values).replace("</", "<\\/")
    await conn.close()

    return result


@app.get("/")
async def home():
    users = await getUsers()
    return users

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getUsers())
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

In this code, you are creating a small FastAPI application that connects to the existing postgresql db. You can run FasAPI apps with uvicorn or gunicorn web servers.

4. Run the application with **`uvicorn app:app --reload`**, open your browser on this page `http://localhost:8000/`. 


## Dockerize FastAPI 
1. Create a **`Dockerfile`** with the following content:

```Docker
FROM python:3.9.7-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip3 install -r requirements.txt

EXPOSE 80

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

```

2. Open **`docker-compose.yaml`** file and add this new service:

```yaml
  fastapi:
    build: .
    container_name: fastapi
    ports:
      - "8084:8000"
```
3. Open `app.py` and modify the host in the connection string with `pg-docker`.

```python
async def getUsers():
    conn = await asyncpg.connect(user='username',password='password',
                                database='db_sample', host='pg-docker')
```

4. Run `docker-compose build` to build the new image.
5. Once it is built, run `docker-compose run` to run all the three containers.
6. Open your browser on this page `http://localhost:8084/`.
7. Also check open a new tab and browse to `http://localhost:8085/` and check the **Users** table under db_sample -> Schemas -> public -> Tables -> users -> View/Edit Data ->  All Rows.
