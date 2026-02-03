from rest_framework import serializers
from ..models import ToDo


class TodoSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(source="user.id", read_only=True)
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = ToDo
        fields = "__all__"
