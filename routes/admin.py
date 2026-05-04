from django.contrib import admin
from .models import Task, User, PushSubscription

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'password',  'email')

admin.site.register(Task)
#admin.site.register(User)
admin.site.register(PushSubscription)

