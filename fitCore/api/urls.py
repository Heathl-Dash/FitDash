from django.urls import path, include
from .views import ToDoViewSet, HabitViewSet, HabitAddPositiveCountView, HabitAddNegativeCountView, ToDoToggleMarkView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'todo', ToDoViewSet, basename='todo')
router.register(r'habit', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('habits/<int:pk>/add-positive-counter/', 
         HabitAddPositiveCountView.as_view(), 
         name="habit-add-positive-counter"
    ),
    path('habits/<int:pk>/add-negative-counter/', 
         HabitAddNegativeCountView.as_view(), 
         name="habit-add-negative-counter"
    ),
    path('todo/<int:pk>/done-toggle/',
        ToDoToggleMarkView.as_view(),
        name="todo-done-toggle"
    ),
]
