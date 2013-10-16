# -*- coding: utf-8 -*- 

from registration.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpResponseRedirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form' : form})
        