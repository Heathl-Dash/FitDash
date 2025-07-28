from django.db import models
from datetime import date
from crum import get_current_user

class FitData(models.Model):
    date=models.DateField(default=date.today)
    steps=models.PositiveBigIntegerField(default=0)
    distance=models.DecimalField(max_digits=8,decimal_places=2)
    burned_calories=models.DecimalField(max_digits=12,decimal_places=4)
    user_id=models.PositiveIntegerField()

    def save(self,*args, **kwargs):
        user=get_current_user()
        print(user)
        return super().save(user_id=user.id)

    
