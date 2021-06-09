from django.views import generic

from .models import Event


class EventList(generic.ListView):
    model = Event
    context_object_name = 'all_events'
    template_name = 'event/index.html'
