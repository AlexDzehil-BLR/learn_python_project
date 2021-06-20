from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .models import Event
from .form import CreateEventForm


def event_list(request):
    events_all = Event.objects.all()
    context = {'events_all': events_all}
    return render(request, 'events/index.html', context)


@login_required(login_url='events:index')
def create_event(request):
    event = Event.objects.get()
    if request.method != 'POST':
        form = CreateEventForm()
    else:
        form = CreateEventForm(data=request.POST)
        if form.is_valid():
            new_event = form.save()
            new_event.save()
            return redirect('accounts:profiles')

    context = {'form': form}
    return render(request, 'events/create_event.html', context)




@login_required(login_url='events:index')
def update_event(request):
    pass

@login_required(login_url='events:index')
def delete_event(request):
    pass
