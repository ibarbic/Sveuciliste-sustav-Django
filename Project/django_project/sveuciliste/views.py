from users.models import Uloge
from django.shortcuts import render


def home(request):
    return render(request, 'home.html', {'title': 'Home'})
