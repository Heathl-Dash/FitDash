from django.urls import path, include
from .viewsets import (
    ToDoViewSet,
    HabitViewSet,
    FitDataViewSet
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'todo', ToDoViewSet, basename='todo')
router.register(r'habit', HabitViewSet, basename='habit')
router.register(r'fitdata', FitDataViewSet, basename='fitdata')


urlpatterns = [
    path("", include(router.urls)),
]
