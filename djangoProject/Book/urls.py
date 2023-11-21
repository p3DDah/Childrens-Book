from django.urls import path
from . import views

urlpatterns = [
    path("", views.AllToDos.as_view(), name="index")
]