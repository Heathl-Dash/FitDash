from django.db import models
from rest_framework.exceptions import ValidationError
from .base import ToDoBase
class ToDo(ToDoBase):
    done=models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=["done","-created"]