from ..serializers import FitDataSerializer,FitDataWeekSerializer
from ..models import FitData,FitDataWeek
from rest_framework.exceptions import PermissionDenied, ValidationError
from crum import get_current_user
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class FitDataViewSet(ModelViewSet):
    serializer_class=FitDataSerializer
    queryset=FitData.objects.all()

    def get_object(self):
        user=get_current_user()
        obj= super().get_object()
        if obj.user_id != user.id:
            raise PermissionDenied("Você não tem permissão para editar essa tarefa!")
        return obj
    
    def get_queryset(self):
        user=get_current_user()
        return FitData.objects.filter(user_id=user.id).order_by("fit_date")
    
    @action(detail=False,methods=["GET"])
    def week(self,request, *args, **kwargs):
        user=get_current_user()
        queryset=FitDataWeek.objects.filter(user_id=user.id)
        serializer=FitDataWeekSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

