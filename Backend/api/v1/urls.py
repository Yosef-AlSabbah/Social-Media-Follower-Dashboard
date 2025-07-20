from django.urls import path, include

app_name = "v1"

urlpatterns = [
    path("metrics/", include("metrics.urls")),
]

