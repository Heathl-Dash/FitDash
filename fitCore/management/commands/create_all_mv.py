from django.core.management.base import BaseCommand
from django.db import connection
from fitCore.materialized_views import base
import importlib
import pkgutil
import fitCore.materialized_views as mvs


def load__all_mviews():
    for _, module_name, _ in pkgutil.iter_modules(mvs.__path__):
        importlib.import_module(f"{mvs.__name__}.{module_name}")


class Command(BaseCommand):
    help = "Cria todas as materialized views registradas"

    def handle(self, *args, **options):
        load__all_mviews()
        for name, mv in base.MV_REGISTRY.items():
            with connection.cursor() as cursor:
                cursor.execute(mv.sql)
            self.stdout.write(f"Materialized View {name} criada com sucesso.")
