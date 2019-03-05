from django.shortcuts import render,redirect


# Create your views here.
def homepage(request):
    return render(request = request,
                  template_name='taskman/home.html')
# Create your views here.
