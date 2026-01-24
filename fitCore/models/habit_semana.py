from django.db import models


class HabitSemana(models.Model):
    user_id = models.UUIDField(editable=False)
    dia = models.DateField()
    total_habits = models.IntegerField()
    habits_positivos = models.IntegerField()
    habits_negativos = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'habit_semana'