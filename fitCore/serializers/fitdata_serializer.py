from rest_framework import serializers
from ..models import FitData, FitDataWeek
from crum import get_current_user


class FitDataSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.id", read_only=True)
    id = serializers.UUIDField(read_only=True)

    def create(self, validated_data):
        user = get_current_user()
        fit_date = validated_data["fit_date"]

        instance, created = FitData.objects.update_or_create(
            user_id=user.id,
            fit_date=fit_date,
            defaults={
                "steps": validated_data["steps"],
                "distance": validated_data["distance"],
                "burned_calories": validated_data["burned_calories"],
            },
        )
        return instance

    class Meta:
        model = FitData
        fields = ["id", "steps", "distance", "burned_calories", "user_id", "fit_date"]


class FitDataWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitDataWeek
        fields = ["id", "steps", "distance", "burned_calories", "user_id", "fit_date"]
