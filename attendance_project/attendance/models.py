from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image
from datetime import date,datetime


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 and img.width > 300:
            output_size = (200, 200)
            img.thumbnail(output_size)
            img.save(self.image.path)


    
class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    admin = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null = False, default = "", blank = True)
    emp_id = models.CharField(max_length=25)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, default='M')
    dob = models.DateField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name}'


class Attendance(models.Model):
    emp_id_attendance = models.ForeignKey(Employee, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField(blank=True, null=True)
    in_time = models.TimeField(blank=True, null=True)
    out_time = models.TimeField(blank=True, null=True)
    duration = models.CharField(max_length=100,blank=True,null=True)
    stats = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.emp_id_attendance.name}'


class LeaveReportEmployee(models.Model):
    LEAVE_CHOICES = (
        ('FD', 'Full Day'),
        ('HD', 'Half Day'),
        ('QD', 'Quater Day')
    )
    emp_id_leave = models.ForeignKey(Employee, on_delete=models.CASCADE)
    attendance_id_leave = models.ForeignKey(Attendance, null=True, on_delete=models.CASCADE)
    from_leave_date = models.DateField(
        blank=True, null=True, default= date.today)
    to_leave_date = models.DateField(
        blank=True, null=True, default= date.today)
    leave_message = models.CharField(max_length=100, blank=True, null=True)
    leave_status = models.CharField(
        max_length=10, choices=LEAVE_CHOICES, default='FD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.emp_id_leave.name}'
