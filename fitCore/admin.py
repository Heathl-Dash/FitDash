from django.contrib import admin
from .models import ToDo, Habit, ToDoSemana, HabitSemana, FitData


admin.site.register(ToDo)
admin.site.register(Habit)
admin.site.register(ToDoSemana)
admin.site.register(HabitSemana)
admin.site.register(FitData)
