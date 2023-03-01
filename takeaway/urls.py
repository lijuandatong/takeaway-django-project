from django.urls import path
from takeaway import views

app_name = "takeaway"

urlpatterns = [
    path("", views.index, name="index"),
]