from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

def home(request):
    return render(request, 'account/base.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'account/signup.html', {'form': UserCreationForm()})
 