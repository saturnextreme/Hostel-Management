# https://github.com/saturnextreme/Hostel-Management
from django.db import models

class Hostel(models.Model):
    roll_no = models.ForeignKey('Student', on_delete=models.CASCADE)
    floor_no = models.CharField(max_length=10)
    room_no = models.ForeignKey('Room', on_delete=models.CASCADE)
    vacancy = models.BooleanField(default=True)
    date_of_join = models.DateField()
    validity = models.DateField()
    boys_girls_block = models.CharField(max_length=10)
    is_present = models.BooleanField(default=True)
    notification = models.TextField()

class Room(models.Model):
    room_no = models.CharField(primary_key=True, max_length=10)
    table = models.BooleanField(default=True)
    chair = models.BooleanField(default=True)
    bed = models.BooleanField(default=True)
    cleaning = models.BooleanField(default=True)
    roll_no = models.ForeignKey('Student', on_delete=models.CASCADE)

class Academics(models.Model):
    roll_no = models.ForeignKey('Student', on_delete=models.CASCADE)
    department = models.CharField(max_length=50)
    course = models.CharField(max_length=50)
    year = models.IntegerField()
    semester = models.IntegerField()

class Student(models.Model):
    roll_no = models.CharField(primary_key=True, max_length=10)
    image = models.ImageField(upload_to=None)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    guardian = models.CharField(max_length=100)
    guardian_mobile_no = models.CharField(max_length=15)
    blood_group = models.CharField(max_length=5)
    age = models.IntegerField()
    email = models.EmailField()
    room_no = models.ForeignKey('Room', on_delete=models.CASCADE)

class EntryExitForm(models.Model):
    roll_no = models.ForeignKey('Student', on_delete=models.CASCADE)
    entry_date = models.DateField()
    exit_date = models.DateField()
    entry_time = models.TimeField()
    exit_time = models.TimeField()
    pnr_no = models.CharField(max_length=20)
    reason_for_leaving = models.TextField()

class Complaint(models.Model):
    roll_no = models.ForeignKey('Student', on_delete=models.CASCADE)
    complaint = models.TextField()
    complaint_by = models.TextField()
    complaint_datetime = models.DateTimeField()
    is_addressed = models.BooleanField(default=False)

class Admin(models.Model):
    username = models.CharField(primary_key=True, max_length=50)
    password = models.CharField(max_length=100)
    notification = models.TextField()
    notification_datetime = models.DateTimeField()
