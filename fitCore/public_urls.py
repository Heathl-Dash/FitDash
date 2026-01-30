from rest_framework.routers import DefaultRouter
from fitCore.viewsets.public.fitdata_viewset import PublicFitDataViewSet
from fitCore.viewsets.public.habit_viewset import PublicHabitViewSet
from fitCore.viewsets.public.todo_viewset import PublicToDoViewSet

router = DefaultRouter()
router.register("fitdata", PublicFitDataViewSet, basename="public-fitdata")
router.register("habits", PublicHabitViewSet, basename="public-habits")
router.register("todos", PublicToDoViewSet, basename="public-todos")

urlpatterns = router.urls
