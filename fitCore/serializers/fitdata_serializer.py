from rest_framework import serializers
from ..models import FitData
from crum import get_current_user


class FitDataSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    id=serializers.IntegerField(read_only=True)

    def create(self, validated_data):
        user=get_current_user()
        fit_date=validated_data['fit_date']

        instance, created=FitData.objects.update_or_create(
            user_id=user.id,
            fit_date=fit_date,
            defaults={
                'steps':validated_data['steps'],
                'distance':validated_data['distance'],
                'burned_calories':validated_data['burned_calories']
            }
        )
        return instance

    class Meta:
        model = FitData
        fields = ['id','steps','distance','burned_calories','user_id','fit_date']