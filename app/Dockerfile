FROM python:latest
ENV DATABASE_URL postgresql://postgres:example@db:5432
ENV SERVER_URL 0.0.0.0:8000/
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
COPY . /app
ENTRYPOINT ["uvicorn", "server:app", "--host 0.0.0.0", "--port 8000"]