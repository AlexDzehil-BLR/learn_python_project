import datetime

from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .form import CreateUserForm, ProfilesForm
from events.models import Event


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
                login(request, user)
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
    events_old = events.filter(event_date__lte=datetime.date.today())
    name = request.user.profiles.name
    email = request.user.profiles.email
    bio = request.user.profiles.bio
    context = {'name': name, 'email': email, 'bio': bio, 'events_now': events_now, 'events_old': events_old}
    return render(request, 'accounts/profile.html', context)



