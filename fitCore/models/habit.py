from django.db import models
from rest_framework.exceptions import ValidationError
from .base import ToDoBase


class Habit(ToDoBase):
    positive = models.BooleanField(default=False)
    negative = models.BooleanField(default=False)
    positive_count = models.PositiveIntegerField(default=0)
    negative_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.positive and not self.negative:
            raise ValidationError(
                "Pelo menos um dos campos 'Positivo' ou 'Negativo' deve ser Verdadeiro"
            )
        super().save(*args, **kwargs)
