from rest_framework import serializers
from ..models import FitData

class FitDataSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model = FitData        
        fields = ['steps','distance','burned_calories','user_id']