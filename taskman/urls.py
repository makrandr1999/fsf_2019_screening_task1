from django.urls import path,include
from . import views

app_name ="taskman"
urlpatterns = [
    path('', views.homepage,name= "homepage"),
    
    ]