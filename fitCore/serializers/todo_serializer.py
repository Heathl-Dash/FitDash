from rest_framework import serializers
from ..models import ToDo

class TodoSerializer(serializers.ModelSerializer):
    user_id=serializers.IntegerField(read_only=True)
    class Meta:
        model = ToDo        
        fields = '__all__'