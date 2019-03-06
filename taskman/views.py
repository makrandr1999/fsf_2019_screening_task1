from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages


# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='taskman/home.html')
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"New Account Created: {username}")
            login(request, user)
            messages.info(request,f"You are now logged in as {username}")

            return redirect("taskman:homepage")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

            return render(request = request,
                          template_name = "taskman/register.html",
                          context={"form":form})

    form = UserCreationForm
    return render(request = request,
                  template_name = "taskman/register.html",
                  context={"form":form})                  
# Create your views here.
