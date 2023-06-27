from .models import Task
from django.shortcuts import render


def home(request):
    context = {
        'tasks': Task.objects.all(),
    }
    return render(request, "app/home.html", context)
