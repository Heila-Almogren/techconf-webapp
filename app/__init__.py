import os
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy 
# from azure.servicebus import QueueClient
from azure.servicebus import ServiceBusClient, ServiceBusMessage


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

app.secret_key = app.config.get('SECRET_KEY')

# queue_client = QueueClient.from_connection_string(app.config.get('SERVICE_BUS_CONNECTION_STRING'),
#                                                  app.config.get('SERVICE_BUS_QUEUE_NAME'))
servicebus_client = ServiceBusClient.from_connection_string(conn_str=app.config.get('SERVICE_BUS_CONNECTION_STRING'), logging_enable=True)
sender = servicebus_client.get_queue_sender(queue_name=app.config.get('SERVICE_BUS_QUEUE_NAME'))
receiver = servicebus_client.get_queue_receiver(queue_name=app.config.get('SERVICE_BUS_QUEUE_NAME'), max_wait_time=5)
with receiver:
        for msg in receiver:
            print("Received: " + str(msg))
            receiver.complete_message(msg)

db = SQLAlchemy(app)

from . import routes