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
    path('dashboard/<int:task_id>/', views.detail, name='detail'),
    
    ]