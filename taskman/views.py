from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Task,Team
from django.http import Http404
from django.http import HttpResponse
from django.db.models import Q
from .forms import TeamForm,TaskForm,CommentForm

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
def create_teams(request):
    if request.method == "POST":
        form = TeamForm(request.POST,initial={'members':request.user})
        if form.is_valid():
            form.save()
            teamname = form.cleaned_data.get('name')
            messages.success(request,f"New Team Created: {teamname}")

            return redirect("taskman:teams")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

            return render(request = request,
                          template_name = "taskman/create-team.html",
                          context={"form":form})

    form = TeamForm
    return render(request = request,
                  template_name = "taskman/create-team.html",
                  context={"form":form})
'''
@login_required
def load_assignees(request):
    id = request.GET.get('team')
    assignees = Team.objects.filter(id=id).values_list('members__username')
    return render(request, 'taskman/assignee_dropdown_list_options.html', {'cities': assignees})                     
'''
@login_required               
def create_tasks(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.creator = request.user
            form.save()
            taskname = form.cleaned_data.get('title')
            messages.success(request,f"New Task Created: {taskname}")

            return redirect("taskman:dashboard")

        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}:{form.error_messages[msg]}")

            return render(request = request,
                          template_name = "taskman/create-task.html",
                          context={"form":form})

    form = TaskForm()
    return render(request = request,
                  template_name = "taskman/create-task.html",
                  context={"form":form})                                            
    
@login_required               
def dashboard(request):
    query_results = Task.objects.filter(Q(assignee=request.user) | Q(creator =request.user)).distinct()

    return render(request = request,
                  template_name='taskman/dashboard.html',context={"tasks":query_results})
@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.creator==request.user:
        if request.method == "POST":
            form = TaskForm(request.POST, instance=task)
            if form.is_valid():
               task.save()
               return redirect('taskman:detail',task_id=task_id)
        else:
            form = TaskForm(instance=task)
            return render(request, 'taskman/create-task.html', {'form': form})      
    else:
        return HttpResponse("Unauthorized Access." )
        
    
@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task,pk=task_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.author=request.user
            comment.save()
            return redirect('taskman:detail',task_id=task_id)
    else:
        form = CommentForm()
    return render(request, 'taskman/add-comment.html', {'form': form})                   

@login_required
def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    #task = Task.objects.filter(id=task_id)
    if request.user in task.assignee.all()  or task.creator == request.user:
        assignees=task.assignee.all()
        return render(request, 'taskman/detail.html', {'task': task,'assignees':assignees})
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
