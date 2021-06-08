from django.shortcuts import render

from .models import Event


def index(request):
    all_events = Event.objects.all()
    context = {'all_events': all_events}
    return render(request, 'event/index.html', context)
