FROM python:3.9-alpine

RUN pip install --upgrade pip
RUN pip install pika

ADD publisher.py /publisher.py

ENV PYTHONUNBUFFERED=1

CMD ["python", "/publisher.py"]