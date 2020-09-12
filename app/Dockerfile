FROM python:latest
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
COPY src/. /app
CMD uvicorn server:app --host 0.0.0.0 --port 8000