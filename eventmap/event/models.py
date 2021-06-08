from django.db import models


class Event(models.Model):
    title = models.CharField(max_length=140)
    owner = models.CharField(max_length=50)
    location = models.CharField(max_length=250)
    # location_lat = models.DecimalField()
    # location_long = models.DecimalField()
    event_text = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    event_date = models.DateTimeField('date event', auto_now=False)

    class Meta:
        verbose_name_plural = 'events'

    def __str__(self):
        return f'<{self.title}:{self.owner}:{self.location}>'
