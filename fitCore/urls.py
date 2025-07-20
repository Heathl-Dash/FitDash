from django.urls import path, include
from .viewsets import (
    ToDoViewSet, 
    HabitViewSet, 
    HabitAddPositiveCountView,
    HabitAddNegativeCountView, 
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'todo', ToDoViewSet, basename='todo')
router.register(r'habit', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
    path('habit/<int:pk>/add-positive-counter/', 
         HabitAddPositiveCountView.as_view(), 
         name="habit-add-positive-counter"
    ),
    path('habit/<int:pk>/add-negative-counter/', 
         HabitAddNegativeCountView.as_view(), 
         name="habit-add-negative-counter"
    )
]
