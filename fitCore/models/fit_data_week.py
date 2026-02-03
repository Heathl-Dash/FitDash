from django.db import models


class FitDataWeek(models.Model):
    fit_date = models.DateField()
    steps = models.PositiveBigIntegerField(default=0)
    distance = models.DecimalField(max_digits=8, decimal_places=2)
    burned_calories = models.DecimalField(max_digits=12, decimal_places=4)
    user_id = models.UUIDField(editable=False)

    class Meta:
        managed = False
        db_table = "fitdata_week"
