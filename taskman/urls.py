from django.urls import path,include
from . import views

app_name ="taskman"
urlpatterns = [
    path('', views.homepage,name= "homepage"),
    path('register/',views.register, name="register"),
    path('logout/',views.logout_request,name="logout"),
    path('login/',views.login_request,name="login"),
    
    ]