from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    employee_ic=models.CharField(max_length=15, primary_key = True)
    employee_name=models.TextField(max_length=255)
    employee_email=models.CharField(max_length=255)
    dob=models.CharField(max_length=50)
    num_phone=models.CharField(max_length=12)
    position=models.TextField(max_length=255)
    department=models.TextField(max_length=255)
    salary=models.CharField(max_length=7)
    emergency_num=models.CharField(max_length=12)
    emergency_name=models.TextField(max_length=255)
    emp_username=models.CharField(max_length=255)
    emp_password=models.CharField(max_length=255)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True, default='profile_pics/default_pic.png')
    total_leave = models.PositiveIntegerField(default=0)  # Add this line

class Leave(models.Model):
    leavetype = models.CharField(max_length=255)
    startdate = models.DateField(blank=True, null=True)
    enddate = models.DateField(blank=True, null=True)
    reason = models.TextField(max_length=255)
    employee_ic = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=10, default="Pending")
    duration = models.PositiveIntegerField(default=0)  # Add this line to store the leave duration
    document = models.FileField(upload_to='leave_documents/', blank=True, null=True)  # Add this line

class Dashboard(models.Model):
    announcement_title = models.CharField(max_length=255)
    announcement_content = models.CharField(max_length=255)
    announcement_date = models.DateField(blank=True, null=True)

class Package(models.Model):
    package_id = models.CharField(max_length=255, primary_key=True)
    package_name = models.CharField(max_length=255)
    price = models.CharField(max_length=7)
    total_date = models.CharField(max_length=2)
    package_detail = models.CharField(max_length=255)
    hotel_name = models.CharField(max_length=255, blank= True, null= True)
    available = models.CharField(max_length=10, default="Available")
    employee_ic = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True)

    
