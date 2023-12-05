from django.views.generic import ListView
from .models import ToDoItem

class AllToDos(ListView):
    model = ToDoItem
    template_name = "template/config.html"