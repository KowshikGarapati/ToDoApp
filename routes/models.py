from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
#from django.contrib.gis.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length= 150, blank= False)
    password = models.CharField(max_length= 150, blank= False)
    default_longitude = models.FloatField(blank=True, null=True)
    default_latitude = models.FloatField(blank=True, null=True)
    email = models.EmailField()

    objects = models.Manager()
    def __str__(self):
        return self.name + self.password


class Task(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "tasks" , null=True, blank=True )
    date = models.DateField()
    time = models.TimeField()
    title = models.CharField(max_length = 150, blank = False)
    description = models.TextField(max_length = 300, blank = False)
    lat = models.FloatField(blank = False)
    lon = models.FloatField(blank = False)
    #location = models.PointField()


