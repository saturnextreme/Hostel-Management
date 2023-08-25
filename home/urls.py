from .views import *
from django.urls import path

urlpatterns = [
    path('', home, name='homepage'),
    path('login', login_warden, name='login_warden')
]