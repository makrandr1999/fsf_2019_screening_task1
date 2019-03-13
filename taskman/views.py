from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Task,Team
from django.http import Http404
from django.http import HttpResponse

# Create your views here.sdfkj486578  Team.objects.filter(members__username='zaccishere')
def homepage(request):
    return render(request = request,
                  template_name='taskman/home.html')

@login_required               
def teams(request):
    query_results = Team.objects.filter(members__username=request.user)
    return render(request = request,
                  template_name='taskman/teams.html',context={"teams":query_results})
    
@login_required               
def dashboard(request):
    query_results = Task.objects.filter(assignee=request.user)

    return render(request = request,
                  template_name='taskman/dashboard.html',context={"tasks":query_results})

@login_required
def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    #task = Task.objects.filter(id=task_id)
    if request.user in task.assignee.all()  or task.creator == request.user:
        return render(request, 'taskman/detail.html', {'task': task})
    else:  
        return HttpResponse("Unauthorized Access %s." %task_id )                   

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"New Account Created: {username}")
            login(request, user)
            messages.info(request,f"You are now logged in as {username}")

            return redirect("taskman:dashboard")

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
def logout_request(request):
    logout(request)
    messages.info(request,"Logged out successfully!")
    return redirect("taskman:homepage")
def login_request(request):
    if request.method == "POST":
        form=AuthenticationForm(request, data= request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user= authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f"You are now logged in as {username}")
                return redirect("taskman:dashboard")
            else:
                messages.error(request,"Invalid username or password")    
        else:
                messages.error(request,"Invalid username or password")            


    form = AuthenticationForm()
    return render(request,"taskman/login.html",{"form":form})    

# Create your views here.
