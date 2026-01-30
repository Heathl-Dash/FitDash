from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from ...models import FitData, FitDataWeek
from ...serializers import FitDataSerializer, FitDataWeekSerializer


class PublicFitDataViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = FitDataSerializer
    queryset = FitData.objects.all()

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")

        if not user_id:
            return FitData.objects.none()

        return (
            FitData.objects
            .filter(user_id=user_id)
            .order_by("fit_date")
        )

    @action(detail=False, methods=["get"])
    def week(self, request):
        user_id = request.query_params.get("user_id")

        if not user_id:
            return Response(
                {"detail": "user_id é obrigatório"},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = FitDataWeek.objects.filter(user_id=user_id)
        serializer = FitDataWeekSerializer(queryset, many=True)
        return Response(serializer.data)
