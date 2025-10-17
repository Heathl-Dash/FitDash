import factory
import random

from datetime import datetime
from fitCore.models.habit import Habit
from fitCore.models.todo import ToDo


class ToDoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ToDo

    title = factory.Faker("word")
    description = factory.Faker("sentence")  
    created = factory.LazyFunction(datetime.now)

class HabitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Habit
    
    title = factory.Faker("word")
    description = factory.Faker("sentence")
    created = factory.LazyFunction(datetime.now)
    @factory.lazy_attribute
    def positive(self):
        return random.choice([True, False])

    @factory.lazy_attribute
    def negative(self):
        return False if self.positive else True
    positive_count = factory.Faker("random_int", min=0, max=100)
    negative_count = factory.Faker("random_int", min=0, max=100)