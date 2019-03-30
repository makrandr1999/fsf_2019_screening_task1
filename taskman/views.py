from django.shortcuts import get_object_or_404, render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import Task,Team,Comment
from django.http import Http404
from django.http import HttpResponse
from django.db.models import Q
from .forms import TeamForm,TaskForm,CommentForm,SelectTeamForm

# Create your views here.sdfkj486578  Team.objects.filter(members__username='zaccishere')
def homepage(request):
    return render(request = request,
                  template_name='taskman/home.html')
                 
@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.username == comment.author:
        comment.delete()
        return redirect('taskman:detail', task_id=comment.task.pk)  
    else:
        return render(request = request,
                  template_name='taskman/unauthorized.html')    


@login_required               
def teams(request):
    query_results = Team.objects.filter(Q(members__username=request.user) | Q(creator =request.user)).distinct()
    return render(request = request,
                  template_name='taskman/teams.html',context={"teams":query_results})
@login_required               
def select_team(request):
    if request.method == "POST":
        form = SelectTeamForm(request,request.POST)
        if form.is_valid():
            team = form.cleaned_data.get('team')
            if team == None:
                teamid= 0
            else:
                teamid=team.id    
            return redirect("taskman:create_tasks",teamid=teamid)

        else:


            return render(request = request,
                          template_name = "taskman/select-team.html",
                          context={"form":form})

    form = SelectTeamForm(request)
    return render(request = request,
                  template_name = "taskman/select-team.html",
                  context={"form":form})
@login_required               
def create_teams(request):
    if request.method == "POST":
        form = TeamForm(request.POST,initial={'members':request.user})
        if form.is_valid():
            team = form.save(commit=False)
            team.creator=request.user
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
def create_tasks(request,teamid):
    team_check=Team.objects.filter(Q(members__username=request.user) | Q(creator =request.user),id=teamid).distinct()
    if team_check or teamid==0:
        if request.method == "POST":
            form = TaskForm(request,teamid,request.POST)
            if form.is_valid():
                submission = form.save(commit=False)
                submission.creator = request.user
                if teamid != 0:
                    submission.team=Team.objects.filter(id=teamid)[0]
                form.save()
                taskname = form.cleaned_data.get('title')
                messages.success(request,f"New Task Created: {taskname}")
                messages.success(request,f"Team ID: {teamid}")

                return redirect("taskman:dashboard")

            else:
                for msg in form.error_messages:
                    messages.error(request, f"{msg}:{form.error_messages[msg]}")

                return render(request = request,
                                template_name = "taskman/create-task.html",
                                context={"form":form})

        form = TaskForm(request=request,teamid=teamid)
        return render(request = request,
                        template_name = "taskman/create-task.html",
                        context={"form":form}) 
    else:
        return render(request = request,
                  template_name='taskman/unauthorized.html')                                                                   
    
@login_required               
def dashboard(request):
    tasks = Task.objects.filter(Q(assignee=request.user) | Q(creator =request.user)).distinct()

    return render(request = request,
                  template_name='taskman/dashboard.html',context={"tasks":tasks})
@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.creator==request.user:
        if request.method == "POST":
            form = TaskForm(task,task.team.id,request.POST)
            if form.is_valid():
               #submission = form.save(commit=False)
               
               task.save()
               messages.info(request,f"new title {task.title}") 
               
               return redirect('taskman:detail',task_id=task_id)
            else:
               for msg in form.error_messages:
                    messages.error(request, f"{msg}:{form.error_messages[msg]}")  
               form = TaskForm(instance=task,teamid=task.team.id,request=request)
               return render(request, 'taskman/create-task.html', {'form': form})        
        else:
            
            form = TaskForm(instance=task,teamid=task.team.id,request=request)
            return render(request, 'taskman/create-task.html', {'form': form})      
    else:
        return render(request = request,
                  template_name='taskman/unauthorized.html')    
        
    
@login_required
def add_comment(request, task_id):
    task = get_object_or_404(Task,pk=task_id)
    if request.user in task.assignee.all()  or task.creator == request.user:
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
    else:
        return render(request = request,
                  template_name='taskman/unauthorized.html')    
                              

@login_required
def detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    #task = Task.objects.filter(id=task_id)
    if request.user in task.assignee.all()  or task.creator == request.user:
        assignees=task.assignee.all()
        return render(request, 'taskman/detail.html', {'task': task,'assignees':assignees})
    else:  
        return render(request = request,
                  template_name='taskman/unauthorized.html')                      

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
