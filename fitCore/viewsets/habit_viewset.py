from ..serializers import HabitSerializer
from ..models import Habit
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ..utils import SheetExporter


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def get_object(self):
        obj = super().get_object()
        if obj.user_id != self.request.user.id:
            raise PermissionDenied("Você não tem permissão para editar essa tarefa!")
        return obj

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

    def get_queryset(self):
        queryset = Habit.objects.filter(user_id=self.request.user.id)
        return queryset

    @action(detail=False, methods=["get"])
    def export(self, request):
        query = self.get_queryset()
        serialized = HabitSerializer(query, many=True)
        exporter = SheetExporter()

        format = request.query_params.get("formato", "csv").lower()

        if format == "csv":
            return exporter.generate_csv_response(serialized.data, "Todo")
        elif format == "xlsx":
            return exporter.generate_xlsx_response(serialized.data, "Todo", "Todo")
        else:
            return Response(
                {"detail": "Formato de arquivo inválido. Use 'csv' ou 'xlsx'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["patch"])
    def add_positive_counter(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        if obj.positive is False:
            raise ValidationError("Não é possível adicionar, pois o hábito é negativo.")
        obj.positive_count = obj.positive_count + 1
        obj.save()

        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["patch"])
    def add_negative_counter(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        if obj.negative is False:
            raise ValidationError("Não é possível adicionar, pois o hábito é positivo.")
        obj.negative_count = obj.negative_count + 1
        obj.save()

        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
