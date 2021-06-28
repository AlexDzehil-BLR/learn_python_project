import datetime

from django.contrib.auth.models import User
from django.http import request
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from .form import CreateUserForm, ProfilesForm
from events.models import Event
from .models import Profiles


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('events:index')
    else:
        if request.method != 'POST':
            form = CreateUserForm()
        else:
            form = CreateUserForm(data=request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('events:index')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('events:index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('events:index')
            else:
                messages.info(request, 'Неверные логин или пароль')

        context = {}
        return render(request, 'accounts/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('events:index')


@login_required(login_url='accounts:login')
def profileSettings(request):
    user = request.user.profiles
    form = ProfilesForm(instance=user)

    if request.method == 'POST':
        form = ProfilesForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/settings.html', context)


@login_required(login_url='accounts:login')
def profilePage(request):
    events = Event.objects.filter(user=request.user)
    events_now = events.filter(event_date__gte=datetime.date.today())
    name = request.user.profiles.name
    email = request.user.profiles.email
    bio = request.user.profiles.bio
    context = {'name': name, 'email': email, 'bio': bio, 'events_now': events_now}
    return render(request, 'accounts/profile.html', context)


def profiles_all(request):
    search_query = request.Get.get('search', '')

    if search_query:
        profiles = Profiles.objects.filter(name__icontains=search_query).exclude(user=request.user)
    else:
        profiles = Profiles.objects.all().exclude(user=request.user)

    paginator = Paginator(profiles, 10)
    

class ProfilesAll(ListView):
    model = Profiles
    template_name = 'accounts/profiles_all.html'
    context_object_name = 'profiles'
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')

        if search_query:
            return Profiles.objects.filter(name__icontains=search_query).exclude(user=self.request.user)
        return Profiles.objects.all().exclude(user=self.request.user)


def user_detail_view(request, pk):
    user_id = get_object_or_404(User, pk=pk)
    events = Event.objects.filter(user_id=pk)
    user_events = events.filter(event_date__gte=datetime.date.today())
    user_profile = Profiles.objects.get(user_id=pk)
    context = {'user': user_id, 'user_events': user_events, 'user_profile': user_profile}
    return render(request, 'accounts/detail.html', context)
