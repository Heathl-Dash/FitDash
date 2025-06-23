from django.db import models
from datetime import datetime
from rest_framework.exceptions import ValidationError

class ToDoBase(models.Model):
    title=models.CharField(max_length=50)
    user_id=models.PositiveIntegerField()
    description=models.TextField()
    created=models.DateTimeField(auto_now_add=True)

    class Meta: 
        abstract=True
        ordering=["-created"]
        

class ToDo(ToDoBase):
    done=models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering=["done","-created"]
class Habit(ToDoBase):
    positive=models.BooleanField(default=False)
    negative=models.BooleanField(default=False)
    positive_count=models.PositiveIntegerField(default=0)
    negative_count=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.positive and not self.negative:
            raise ValidationError("Pelo menos um dos campos 'Positivo' ou 'Negativo' deve ser Verdadeiro")
        super().save(*args, **kwargs)