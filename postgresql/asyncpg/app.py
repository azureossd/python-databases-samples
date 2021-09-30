from fastapi import FastAPI
import asyncpg, asyncio, json, uvicorn

app = FastAPI()

async def getUsers():
    conn = await asyncpg.connect(user='username',password='password',
                                database='db_sample', host='pg-docker')

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