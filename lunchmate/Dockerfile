FROM python:3.12-slim
RUN apt-get update
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
EXPOSE 8000