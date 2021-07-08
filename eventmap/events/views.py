import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import Event
from .form import CreateEventForm


def event_list(request):
    events_all = Event.objects.all().filter(event_date__gte=datetime.date.today()).order_by('event_date')
    context = {'events_all': events_all}
    return render(request, 'events/index.html', context)


@login_required(login_url='events:index')
def create_event(request):
    if request.method != 'POST':
        form = CreateEventForm()
    else:
        form = CreateEventForm(data=request.POST)
        if form.is_valid():
            new_event = form.save(commit=False)
            new_event.user = request.user
            new_event.save()
            return redirect('accounts:profile')

    context = {'form': form}
    return render(request, 'events/create_event.html', context)


@login_required(login_url='events:index')
def edit_event(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method != 'POST':
        form = CreateEventForm(instance=event)
    else:
        form = CreateEventForm(instance=event, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')

    context = {'event': event, 'form': form}
    return render(request, 'events/edit_event.html', context)


@login_required(login_url='events:index')
def delete_event(request, event_id):
    event = Event.objects.get(id=event_id)
    event.delete()
    return redirect('accounts:profile')


