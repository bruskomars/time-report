from django.contrib import admin
from .models import User, DailyReport, GeneratedReport, Task, Client, Group, TaskStatus, GeneratedTaskStatus

# Register your models here.
admin.site.register(Task)
admin.site.register(GeneratedReport)
admin.site.register(User)
admin.site.register(DailyReport)
admin.site.register(Client)
admin.site.register(Group)
admin.site.register(TaskStatus)
admin.site.register(GeneratedTaskStatus)