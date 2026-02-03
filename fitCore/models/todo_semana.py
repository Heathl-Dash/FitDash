from django.db import models


class ToDoSemana(models.Model):
    user_id = models.UUIDField(editable=False)
    dia = models.DateField()
    total_todos = models.IntegerField()
    todos_concluidos = models.IntegerField()

    class Meta:
        managed = False
        db_table = "todo_semana"
