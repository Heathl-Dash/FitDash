import factory
import random

from datetime import date, datetime
from fitCore.models.habit import Habit
from fitCore.models.todo import ToDo
from fitCore.models.fit_data import FitData


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

class FitDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FitData

    fit_date = factory.LazyFunction(date.today)
    steps = factory.Faker("random_int", min=1000, max=15000)
    distance = factory.LazyAttribute(lambda o: round(o.steps * 0.0008, 2)) 
    burned_calories = factory.LazyAttribute(lambda o: round(o.steps * 0.04, 2))