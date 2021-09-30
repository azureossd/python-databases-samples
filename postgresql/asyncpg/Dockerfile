FROM python:3.9.7-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip3 install -r requirements.txt

EXPOSE 80

COPY . .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
