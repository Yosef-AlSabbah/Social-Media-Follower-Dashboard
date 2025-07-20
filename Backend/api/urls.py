from django.urls import path, include
from . import views

app_name = "api"

urlpatterns = [
    path("health/", views.health_check, name="health_check"),
    path("v1/", include("api.v1.urls")),
]
