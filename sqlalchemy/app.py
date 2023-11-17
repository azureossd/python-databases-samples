from flask import Flask, jsonify
from models import Task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import os

app = Flask(__name__)


HOST = os.environ.get('HOST')
DATABASE = os.environ.get('DATABASE')
USER = os.environ.get('USER')
PASSWORD = os.environ.get('PASSWORD')

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}/{DATABASE}?charset=utf8mb4", echo=False, pool_pre_ping=True, pool_size=128)
Session = sessionmaker(bind=engine)

messages = []


@app.route('/api/get')
def queryAllRows():
    session = Session()
    tasks = session.query(Task).all()

    all_tasks = [
        {
            "id": t.id,
            "name": t.name,
        }
        for t in tasks
    ]

    session.close()
    print(all_tasks)
    return {"results": all_tasks}


@app.route('/api/insert')
def insertRow():
    session = Session()
    insert_task = Task(name="mow the grass", completed=False)

    session.add(insert_task)
    session.commit()
    session.close()
    return {"results": "inserted"}


@app.route('/api/delete/{id}')
def deleteRow():
    session = Session()
    id = session.query(Task).filter_by(id=id).first()

    session.delete(id)
    session.commit()

    session.close()
    return {"results": "deleted"}


@app.route('/')
def home():
    return jsonify({"msg": "python-database-samples-sqlalchemy"})


if __name__ == '__main__':
    app.run()
