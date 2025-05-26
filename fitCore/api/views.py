from .serializers import TodoSerializer,HabitSerializer
from ..models import ToDo
from rest_framework.generics import  ListAPIView

class ToDoListView(ListAPIView):
    serializer_class=TodoSerializer
    queryset=ToDo.objects.all()
    