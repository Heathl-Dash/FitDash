from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny

from ...models import Habit
from ...serializers import HabitSerializer


class PublicHabitViewSet(ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")

        if not user_id:
            return Habit.objects.none()

        return Habit.objects.filter(user_id=user_id)
