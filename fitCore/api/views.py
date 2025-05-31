from .serializers import TodoSerializer,HabitSerializer
from ..models import ToDo
from rest_framework.generics import  ListAPIView

class ToDoListView(ListAPIView):
    serializer_class=TodoSerializer
    queryset=ToDo.objects.all()

    def get_queryset(self):
        user_id=self.request.user.id
        print(user_id)
        return ToDo.objects.filter(user_id=user_id)
        
    