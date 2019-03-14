from django.urls import path,include
from . import views

app_name ="taskman"
urlpatterns = [
    path('', views.homepage,name= "homepage"),
    path('register/',views.register, name="register"),
    path('logout/',views.logout_request,name="logout"),
    path('login/',views.login_request,name="login"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('teams/',views.teams,name="teams"),
    path('create-team/',views.create_teams,name="create_teams"),
    path('create-task/',views.create_tasks,name="create_tasks"),
    path('dashboard/<int:task_id>/', views.detail, name='detail'),
    
    ]