from rest_framework import serializers
from ..models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.id", read_only=True)

    class Meta:
        model = Habit
        fields = "__all__"
