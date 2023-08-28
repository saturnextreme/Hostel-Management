from django.shortcuts import render

# Create your views here.

# @login_required(login_url='home/homepage.html')
def home(request):
    return render(request, 'home/homepage.html')

def login(request):
    return render(request, 'home/login.html')