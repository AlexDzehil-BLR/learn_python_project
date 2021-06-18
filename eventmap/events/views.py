from django.shortcuts import render

from .models import Event


# Create your views here.
def event_list(request):
    events_all = Event.objects.all()
    context = {'events_all': events_all}
    return render(request, 'events/index.html', context)


def create_event(request):
    pass


def update_event(request):
    pass


def delete_event(request):
    pass
