from django.db import models
#from django.contrib.gis.db import models

# Create your models here.

class Task(models.Model):
    date = models.DateField()
    time = models.TimeField()
    title = models.CharField(max_length = 150, blank = False)
    description = models.TextField(max_length = 300, blank = False)
    lat = models.FloatField(blank = False)
    lon = models.FloatField(blank = False)
    #location = models.PointField()

