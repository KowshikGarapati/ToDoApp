from django.contrib import admin
from .models import Task, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'password', 'default_longitude', 'default_latitude', 'email')

admin.site.register(Task)
#admin.site.register(User)

