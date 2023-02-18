FROM python:3.9-alpine

RUN pip install --upgrade pip
RUN pip install pika

ADD publisher.py /publisher.py

CMD ["python", "/publisher.py"]