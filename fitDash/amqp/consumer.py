import os
import pika
import json
import django
from fitCore.models import Habit, ToDo 
RABBITMQ_DEFAULT_HOST = os.getenv("RABBITMQ_DEFAULT_HOST")
RABBITMQ_DEFAULT_USER = os.getenv("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.getenv("RABBITMQ_DEFAULT_PASS")
RABBITMQ_DEFAULT_VHOST = os.getenv("RABBITMQ_DEFAULT_VHOST")
RABBITMQ_DEFAULT_QUEUE = os.getenv("RABBITMQ_DEFAULT_PORT")
RABBITMQ_QUEUE=os.getenv("RABBITMQ_QUEUE")

os.environ.setdefault("DJANGOSETTINGS_MODULE",'fitDash.settings')
django.setup()


def __get_connection_and_channel():
    credentials=pika.PlainCredentials(RABBITMQ_DEFAULT_USER,RABBITMQ_DEFAULT_PASS)
    parameters=pika.ConnectionParameters(
        host=RABBITMQ_DEFAULT_HOST,
        virtual_host=RABBITMQ_DEFAULT_VHOST,
        credentials=credentials
    )
    connection=pika.BlockingConnection(parameters)
    channel=connection.channel()

    return connection,channel



def start_delete_user_objects():
    conn,chan=__get_connection_and_channel()
    chan.queue_declare(RABBITMQ_QUEUE,durable=True)

    def callback(ch,method,properties,body):
        try:
            data=json.loads(body)
            user_id=data.get("user_id")
            if user_id is not None:
                Habit.objects.filter(user_id=user_id).delete()
                ToDo.objects.filter(user_id=user_id).delete()
        except Exception as e:
            print(f'Erro: {e}')
    chan.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=True
    )

    chan.start_consuming()