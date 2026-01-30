from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/fit/", include("fitCore.urls")),
    path("api/v1/fit/public/", include("fitCore.public_urls")),
]
