FROM python:3.5
ENV PYTHONUNBUFFERED 1
WORKDIR /app
ADD requirements.txt /app/
RUN pip install -r requirements.txt
ADD . /app/