from rest_framework import serializers
from ..models import ToDo,Habit

class TodoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ToDo        
        fields = '__all__'

class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit        
        fields = '__all__'