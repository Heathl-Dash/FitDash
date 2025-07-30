from django.core.management.base import BaseCommand
from fitDash.amqp.consumer import start_delete_user_objects


class Command(BaseCommand):
    help = "inicia o consumidor de eventos, verificando se usuários foram excluidos"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("iniciando consumer"))
        try:
            start_delete_user_objects()
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING("interrompendo comando manualmente"))
