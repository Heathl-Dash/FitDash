from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny

from ...models import ToDo
from ...serializers import TodoSerializer


class PublicToDoViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = TodoSerializer
    queryset = ToDo.objects.all()

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")

        if not user_id:
            return ToDo.objects.none()

        return ToDo.objects.filter(user_id=user_id)
