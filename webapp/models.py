from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# Create your models here.


class User(AbstractUser):
    first_name = models.CharField(max_length=200, null=True)
    last_name = models.CharField(max_length=200, null=True)
    employee_id = models.CharField(max_length=20, unique=True, null=True)
    # avatar = models.ImageField(null=True, default='avatar.svg')

    USERNAME_FIELD = 'employee_id'
    REQUIRED_FIELDS = ['username']


class Task(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Client(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Group(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class DailyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    area_extent = models.CharField(max_length=500, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    date = models.DateField(default=datetime.date.today())
    time_start = models.TimeField(auto_now=False, auto_now_add=False, null=True, default="08:00")
    # time_end = models.TimeField(auto_now=False, auto_now_add=False, null=True, default="17:00")
    time_end = models.CharField(max_length=50, null=True, blank=True)
    total_time = models.CharField(max_length=50)
    status = models.CharField(max_length=200, null=True)
    l_hd = models.CharField(max_length=125, null=True, blank=True)

    class Meta:
        ordering = ['user', 'date']


class TaskStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    area_extent = models.CharField(max_length=500, blank=True, null=True)
    count = models.CharField(max_length=500, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    ijo_no = models.CharField(max_length=500, null=True, blank=True)
    date_start = models.DateField(default=datetime.date.today())
    date_finish = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=500, null=True)
    progress = models.CharField(max_length=500, null=True, blank=True)
    pts_ref = models.CharField(max_length=500, null=True, blank=True)
    invoice = models.CharField(max_length=500, null=True, blank=True)
    remarks = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        ordering = ['date_start']

    def __str__(self):
        return self.name


class GeneratedReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    task = models.CharField(max_length=500)
    area_extent = models.CharField(max_length=500)
    client = models.CharField(max_length=500)
    date = models.DateField(default=datetime.date.today())
    time_start = models.TimeField(null=True, blank=True)
    time_end = models.CharField(max_length=50, null=True, blank=True)
    total_time = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    l_hd = models.CharField(max_length=125, blank=True, null=True)


class GeneratedTaskStatus(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    area_extent = models.CharField(max_length=500, blank=True, null=True)
    count = models.CharField(max_length=500, blank=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    ijo_no = models.CharField(max_length=500, blank=True, null=True)
    date_start = models.DateField(default=datetime.date.today())
    date_finish = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=500, blank=True, null=True)
    progress = models.CharField(max_length=500, blank=True, null=True)
    pts_ref = models.CharField(max_length=500, blank=True, null=True)
    invoice = models.CharField(max_length=500, blank=True, null=True)
    remarks = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['date_start']

