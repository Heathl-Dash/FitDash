from django.db import models

class ToDoBase(models.Model):
    title=models.CharField(max_length=50)
    user_id=models.PositiveIntegerField()
    description=models.TextField()
    created=models.DateTimeField(auto_now_add=True)

    class Meta: 
        abstract=True
        ordering=["-created"]