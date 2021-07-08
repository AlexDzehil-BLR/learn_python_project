from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    TYPE_OF_EVENT = [
        ('o', 'Остальные'),
        ('s', 'Спорт'),
        ('c', 'Культура'),
        ('e', 'Образование'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=140)
    text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    event_date = models.DateTimeField('date event', auto_now=False)
    location = models.CharField(max_length=140)
    location_lat = models.FloatField()
    location_long = models.FloatField()
    type_of_event = models.CharField(max_length=1, choices=TYPE_OF_EVENT, default='o')

    class Meta:
        verbose_name_plural = 'events'

    def __str__(self):
        return f'<{self.title}:{self.user}>'
