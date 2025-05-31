from rest_framework import serializers
from ..models import ToDo,Habit

class TodoSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model = ToDo        
        fields = '__all__'

class HabitSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model = Habit        
        fields = '__all__'