from django.contrib import admin
from .models import User, Task, Team

admin.site.register(User)
admin.site.register(Team)
admin.site.register(Task)
