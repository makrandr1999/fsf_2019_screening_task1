from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages


# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='taskman/home.html')
# Create your views here.
