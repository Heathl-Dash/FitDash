from .serializers import TodoSerializer,HabitSerializer
from ..models import ToDo, Habit
from rest_framework.viewsets import ModelViewSet

class ToDoViewSet(ModelViewSet):
    serializer_class=TodoSerializer
    queryset=ToDo.objects.all()

class HabitViewSet(ModelViewSet):
    serializer_class=HabitSerializer
    queryset=Habit.objects.all()



