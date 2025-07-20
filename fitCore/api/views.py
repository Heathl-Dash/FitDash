from .serializers import TodoSerializer, HabitSerializer
from ..models import ToDo, Habit
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from ..utils import SheetExporter

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

    @action(detail=False,methods=['get'])
    def export(self,request):
        query=self.get_queryset()
        serialized=TodoSerializer(query,many=True)
        exporter=SheetExporter()

        format=request.query_params.get('formato', 'csv').lower()

        if format=='csv':
            return exporter.generate_csv_response(serialized.data,'Todo')
        elif format=='xlsx':
            return exporter.generate_xlsx_response(serialized.data,'Todo','Todo')
        else:
            return Response(
                {"detail": "Formato de arquivo inválido. Use 'csv' ou 'xlsx'."},
                status=status.HTTP_400_BAD_REQUEST
            )

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


class HabitAddPositiveCountView(UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()
        
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("Você não tem permissão para editar essa tarefa!")
        
        if instance.positive == False:
            raise ValidationError("Não é possível adicionar, pois o hábito é negativo.")

        serializer.save(positive_count=instance.positive_count + 1)


class HabitAddNegativeCountView(UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()
        
        if instance.user_id != self.request.user.id:
            raise PermissionDenied("Você não tem permissão para editar essa tarefa!")
        
        if instance.negative == False:
            raise ValidationError("Não é possível adicionar, pois o hábito é positivo.")

        serializer.save(negative_count=instance.negative_count + 1)


class ToDoToggleMarkView(UpdateAPIView):
    serializer_class = TodoSerializer
    queryset = ToDo.objects.all()

    def perform_update(self, serializer):
        instance = self.get_object()

        if instance.user_id != self.request.user.id:
            raise PermissionDenied("Você não tem permissão para editar essa tarefa!")
        
        serializer.save(done=not instance.done)