from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

# @login_required(login_url='home/homepage.html')
def home(request):
    return render(request, 'home/homepage.html')

def login_warden(request):
    return render(request, 'home/login_warden.html')