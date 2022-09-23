FROM python:3.10.7-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 7000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:7000"]
