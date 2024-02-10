from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('signup', signup, name='signup'),
    path('dashboard', dashboard, name='dashboard'),
    path('complaints', complaints, name='complaints'),
    path('notification', notification, name='notification'),
    path('leaveform', leaveform, name='leaveform'),
    path('leaveformstatus', leaveformstatus, name='leaveformstatus'),
    path('profile', profile, name='profile'),
    path('edit_profile', edit_profile, name='edit_profile'),
    path('admin_login', admin_login, name='admin_login'),
    path('admin_signup', admin_signup, name='admin_signup'),
    path('admin_dashboard', admin_dashboard, name='admin_dashboard'),
    path('student_detail', student_detail, name='student_detail'),
    path('admin_notification', admin_notification, name='admin_notification'),
    path('admin_complaint', admin_complaint, name='admin_complaint'),
    path('admin_leaveform', admin_leaveform, name='admin_leaveform'),
    path('student_detail/view/<str:parameter>/', viewprofile, name='viewprofile')
]

