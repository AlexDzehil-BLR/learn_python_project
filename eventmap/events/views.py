from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView
from django.db.models import Q

from .models import Event
from .form import CreateEventForm


# def event_list(request):
#     events_all = Event.objects.all().filter(event_date__gte=datetime.date.today()).order_by('event_date')
#     context = {'events_all': events_all}
#     return render(request, 'events/index.html', context)


class EventList(ListView):
    model = Event
    template_name = 'events/index.html'
    context_object_name = 'events_all'

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')

        if search_query:
            return Event.objects.filter(
                Q(title__icontains=search_query) |
                Q(text__icontains=search_query) |
                Q(event_date__icontains=search_query) |
                Q(location__icontains=search_query) |
                Q(type_of_event__icontains=search_query)
            )
        return Event.objects.all()


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


def json(request):
    data = Event.objects.all()
    data_1 = serialize('json', data, fields=('title', 'text', 'location', 'location_lat', 'location_long'))
    return HttpResponse(data_1, content_type='application/json')

