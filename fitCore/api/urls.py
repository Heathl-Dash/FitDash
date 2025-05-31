from django.urls import path, include
from .views import ToDoViewSet, HabitViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'todo', ToDoViewSet, basename='todo')
router.register(r'habit', HabitViewSet, basename='habit')

urlpatterns = [
    path('', include(router.urls)),
]
