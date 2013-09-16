# -*- coding: utf-8 -*- 

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from django.shortcuts import render

class CreateUserView(CreateView):
    model = User

def register(request):
    form = UserCreationForm()
    return render(request, 'registration/register.html', {'form' : form})