from django.db import models

class ToDoBase(models.Model):
    tittle=models.CharField(max_length=50)
    user_id=models.PositiveIntegerField()
    description=models.TextField()

    class Meta: 
        abstract=True

class ToDo(ToDoBase):
    done=models.BooleanField(default=False)
    everyday= models.BooleanField(default=False)

class Habit(ToDoBase):
    positive=models.BooleanField(default=False)
    negative=models.BooleanField(default=False)
    positive_count=models.PositiveIntegerField(default=0)
    negative_count=models.PositiveIntegerField(default=0)