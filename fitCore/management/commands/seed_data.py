import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from ...models import ToDo, Habit, FitData
from fitCore.seeds.constants import USER_IDS

fake = Faker("pt_BR")


class Command(BaseCommand):
    help = "Popula o banco com dados fake para load test"

    def handle(self, *args, **options):
        self.stdout.write("Gerando dados fake...")

        self.create_todos(3000)
        self.create_habits(1500)
        self.create_fitdata(5000)

        self.stdout.write(self.style.SUCCESS("Dados gerados com sucesso!"))

    def random_user(self):
        return random.choice(USER_IDS)

    def create_todos(self, total):
        todos = []
        for _ in range(total):
            todos.append(
                ToDo(
                    title=fake.sentence(nb_words=4),
                    description=fake.text(max_nb_chars=120),
                    done=fake.boolean(),
                    user_id=self.random_user(),
                )
            )
        ToDo.objects.bulk_create(todos, batch_size=500)
        self.stdout.write(f"{total} ToDos criados")

    def create_habits(self, total):
        habits = []
        for _ in range(total):
            positive = fake.boolean()
            negative = not positive if fake.boolean() else positive

            habits.append(
                Habit(
                    title=fake.word().capitalize(),
                    description=fake.sentence(),
                    positive=positive,
                    negative=negative,
                    positive_count=random.randint(0, 50),
                    negative_count=random.randint(0, 50),
                    user_id=self.random_user(),
                )
            )
        Habit.objects.bulk_create(habits, batch_size=500)
        self.stdout.write(f"{total} Habits criados")

    def create_fitdata(self, total):
        fit_data = []
        today = timezone.now().date()

        for _ in range(total):
            fit_data.append(
                FitData(
                    fit_date=today - timedelta(days=random.randint(0, 365)),
                    steps=random.randint(0, 20000),
                    distance=round(random.uniform(0.5, 15.0), 2),
                    burned_calories=round(random.uniform(100, 1200), 4),
                    user_id=self.random_user(),
                )
            )
        FitData.objects.bulk_create(fit_data, batch_size=500)
        self.stdout.write(f"{total} FitData criados")
