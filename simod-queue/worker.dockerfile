FROM python:3.9-alpine

RUN pip install --upgrade pip
RUN pip install kubernetes pika

ADD worker.py /worker.py

ENV PYTHONUNBUFFERED=1

CMD ["python", "/worker.py"]