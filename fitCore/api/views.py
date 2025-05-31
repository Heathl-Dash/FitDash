from .serializers import TodoSerializer,HabitSerializer
from ..models import ToDo, Habit
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

class ToDoViewSet(ModelViewSet):
    serializer_class=TodoSerializer
    queryset=ToDo.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("Você não tem permissão para editar essa tarefa!")

        serializer.save(user_id=instance.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("Você não tem permissão para editar essa tarefa!")

        instance.delete()

    def get_queryset(self):
        queryset = ToDo.objects.filter(user_id = self.request.user.id)
        return queryset

class HabitViewSet(ModelViewSet):
    serializer_class=HabitSerializer
    queryset=Habit.objects.all()
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("Você não tem permissão para editar essa tarefa!")

        serializer.save(user_id=instance.user_id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def perform_destroy(self, instance):
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("Você não tem permissão para editar essa tarefa!")

        instance.delete()

    def get_queryset(self):
        queryset = Habit.objects.filter(user_id = self.request.user.id)
        return queryset