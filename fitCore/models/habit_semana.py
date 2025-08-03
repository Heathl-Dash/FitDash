from django.db import models


class HabitSemana(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True)
    dia = models.DateField()
    total_habits = models.IntegerField()
    habits_positivos = models.IntegerField()
    habits_negativos = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'habit_semana'