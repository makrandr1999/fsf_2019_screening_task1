from django.urls import path,include
from . import views
from .models import Task,Team,Comment


app_name ="taskman"
urlpatterns = [
    path('', views.homepage,name= "homepage"),
    path('register/',views.register, name="register"),
    path('logout/',views.logout_request,name="logout"),
    path('login/',views.login_request,name="login"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('teams/',views.teams,name="teams"),
    path('create-team/',views.create_teams,name="create_teams"),
    path('create-task/<int:teamid>/',views.create_tasks,name="create_tasks"),
    path('dashboard/<int:task_id>/', views.detail, name='detail'),
    path('dashboard/<int:task_id>/edit', views.task_edit, name='task_edit'),
    path('dashboard/<int:task_id>/comment', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/', views.comment_remove, name='comment_remove'),
    path('select-team/', views.select_team, name='select_team'),

    
    
    ]