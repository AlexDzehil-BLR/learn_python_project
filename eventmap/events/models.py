from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    event_date = models.DateTimeField('date event', auto_now=False)
    location = models.CharField(max_length=140)
    location_lat = models.FloatField()
    location_long = models.FloatField()

    class Meta:
        verbose_name_plural = 'events'

    def __str__(self):
        return f'<{self.title}:{self.user}>'
