from django.core.management.base import BaseCommand
from django.db import connection
from fitCore.materialized_views import base
import importlib
import pkgutil
import fitCore.materialized_views as mvs


def load_all_views():
    for _, module_name, _ in pkgutil.iter_modules(mvs.__path__):
        importlib.import_module(f"{mvs.__name__}.{module_name}")


class Command(BaseCommand):
    help = "Atualiza todas as materialized views registradas."

    def add_arguments(self, parser):
        parser.add_argument(
            "--only", type=str, help="Atualiza apenas a view especificada"
        )
        parser.add_argument(
            "--frequency",
            type=str,
            choices=["daily", "weekly", "monthly"],
            help="Atualiza views por frequência",
        )

    def handle(self, *args, **options):
        load_all_views()
        only = options["only"]
        frequency = options["frequency"]

        updated = 0

        for name, mv in base.MV_REGISTRY.items():
            if only and only != name:
                continue
            if frequency and mv.frequency != frequency:
                continue
            with connection.cursor() as cursor:
                cursor.execute(f"REFRESH MATERIALIZED VIEW {name}")
            self.stdout.write(
                self.style.SUCCESS(f"View '{name}' atualizada com sucesso.")
            )
            updated += 1

        if updated == 0:
            self.stdout.write(
                self.style.WARNING("Nenhuma materialized view foi atualizada.")
            )
