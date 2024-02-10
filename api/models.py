from django.db import models
from django import forms
import datetime
# Create your models here.

def student_image_filename(instance, filename):
    rollno = instance.rollno
    extension = filename.split('.')[-1] 
    new_filename = f'{rollno}.{extension}' 
    return f'student_profiles/{instance.rollno}/{new_filename}'

def ticket_pdf_filename(instance, filename):
    rollno = instance.rollno.rollno
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y%m%d%H%M%S")
    extension = filename.split('.')[-1] 
    new_filename = f'{rollno}_{formatted_datetime}.{extension}' 
    return f'pdfs/ticket/{rollno}/{new_filename}'

def final_pdf_filename(instance, filename):
    rollno = instance.rollno.rollno
    now = datetime.datetime.now()
    formatted_datetime = now.strftime("%Y%m%d%H%M%S")
    extension = filename.split('.')[-1] 
    new_filename = f'{rollno}_{formatted_datetime}.{extension}' 
    return f'pdfs/form/{rollno}/{new_filename}'

class Student(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.CharField(max_length=20)
    password = models.CharField(max_length=150)
    rollno = models.CharField(primary_key=True, unique=True)
    dob = models.CharField(max_length=20)
    sudent_mob = models.CharField(max_length=15)
    father_mob = models.CharField(max_length=15)
    mother_mob =  models.CharField(max_length=15)
    permanent_address = models.TextField()
    image = models.ImageField(upload_to=student_image_filename, blank=True, null=True)

class Admin(models.Model):
    username = models.CharField(primary_key=True, max_length=100)
    password = models.CharField(max_length=150)

class Academics(models.Model):
    rollno = models.ForeignKey(Student, on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    semester = models.CharField(max_length=15)
    course = models.CharField(max_length=10)
    year = models.CharField(max_length=4)

class Hostel(models.Model):
    rollno = models.ForeignKey(Student, on_delete=models.CASCADE)
    room = models.IntegerField()
    bg_block = models.CharField(max_length=1)

class Complaints(models.Model):
    rollno = models.ForeignKey(Student, on_delete=models.CASCADE)
    isverified = models.BooleanField(default=False)
    complaint = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    username = models.ForeignKey(Admin, on_delete=models.CASCADE)
    notice = models.TextField()
    created_at = models.CharField(max_length=30)

class LeaveForm(models.Model):
    form_acceptance = models.CharField(max_length=15)
    reason = models.TextField(null=True)
    leave_date = models.CharField(max_length=12)
    leave_time = models.CharField(max_length=10)
    arrive_date = models.CharField(max_length=12)
    arrive_time = models.CharField(max_length=10)
    rollno = models.ForeignKey(Student, on_delete=models.CASCADE)
    reservation = models.FileField(upload_to=ticket_pdf_filename)
    form = models.FileField(upload_to=final_pdf_filename)
    created_at = models.DateTimeField(auto_now_add=True)


