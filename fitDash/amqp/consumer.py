import os
import pika
import json
from time import sleep
import django
from pika.exceptions import AMQPConnectionError
from fitCore.models import Habit, ToDo

RABBITMQ_DEFAULT_HOST = os.getenv("RABBITMQ_DEFAULT_HOST")
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_VHOST = os.getenv("RABBITMQ_DEFAULT_VHOST")
RABBITMQ_DEFAULT_PORT = os.getenv("RABBITMQ_DEFAULT_PORT")
RABBITMQ_EXCHANGE_NAME = os.getenv("RABBITMQ_EXCHANGE_NAME")
RABBITMQ_EXCHANGE_TYPE = os.getenv("RABBITMQ_EXCHANGE_TYPE")
RABBITMQ_QUEUE_NAME = os.getenv("RABBITMQ_QUEUE_NAME")

os.environ.setdefault("DJANGOSETTINGS_MODULE", "fitDash.settings")
django.setup()


def __get_connection_and_channel():
    credentials = pika.PlainCredentials(RABBITMQ_DEFAULT_USER, RABBITMQ_DEFAULT_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_DEFAULT_HOST,
        port=int(RABBITMQ_DEFAULT_PORT),
        virtual_host=RABBITMQ_DEFAULT_VHOST,
        credentials=credentials,
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    return connection, channel


def start_delete_user_objects():
    retry_timer = 5
    while True:
        try:
            _, chan = __get_connection_and_channel()

            chan.exchange_declare(
                exchange=RABBITMQ_EXCHANGE_NAME,
                exchange_type=RABBITMQ_EXCHANGE_TYPE,
                durable=True,
            )

            chan.queue_declare(RABBITMQ_QUEUE_NAME, durable=True)
            chan.queue_bind(exchange=RABBITMQ_EXCHANGE_NAME, queue=RABBITMQ_QUEUE_NAME)

            def callback(ch, method, properties, body):
                print("mensagem recebida")
                try:
                    data = json.loads(body)
                    user_id = data.get("user_id")
                    event = data.get("event")
                    if user_id is not None and event == "delete":
                        Habit.objects.filter(user_id=user_id).delete()
                        ToDo.objects.filter(user_id=user_id).delete()
                except Exception as e:
                    print(f"Erro: {e}")

            chan.basic_consume(
                queue=RABBITMQ_QUEUE_NAME, on_message_callback=callback, auto_ack=True
            )

            chan.start_consuming()
        except AMQPConnectionError as e:
            print(f"falha de conexão com rabbitMQ: {e}, reiniciando conexão")
            sleep(retry_timer)
        except Exception as e:
            print(f"falha inesperada: {e}, reiniciando conexão")
            sleep(retry_timer)
