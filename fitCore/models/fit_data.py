from django.db import models
from crum import get_current_user


class FitData(models.Model):
    fit_date=models.DateField()
    steps=models.PositiveBigIntegerField(default=0)
    distance=models.DecimalField(max_digits=8,decimal_places=2)
    burned_calories=models.DecimalField(max_digits=12,decimal_places=4)
    user_id=models.UUIDField(editable=False)

    def save(self,*args, **kwargs):
        if not self.user_id:
            user=get_current_user()
            if user:
                self.user_id=user.id
        return super().save(*args, **kwargs)

    
