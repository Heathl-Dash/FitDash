from rest_framework.response import Response
from rest_framework import status
from ..utils import SheetExporter
from rest_framework.decorators import action
from ..serializers import TodoSerializer
from ..models import ToDo
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
    
    @action(detail=True,methods=['patch'])
    def done_toggle(self,request,pk=None):
        instance = self.get_object()
        instance.done=not instance.done
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data,status=status.HTTP_200_OK)