from django.db import models

class User(models.Model):
    name = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    email = models.EmailField()

    def __str__(self):
        return self.name


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=300)
    lat = models.FloatField()
    lon = models.FloatField()


class PushSubscription(models.Model):
    """
    Each record represents ONE device/browser
    linked to a specific user
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    endpoint = models.TextField(unique=True)
    auth = models.CharField(max_length=255)
    p256dh = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.name} -> {self.endpoint[:30]}"
