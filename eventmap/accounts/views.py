import datetime

from django.contrib.auth.models import User
from django.views.generic import ListView
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .form import CreateUserForm, ProfilesForm
from events.models import Event
from .models import Profiles
from itertools import chain


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
    events_now = events.filter(event_date__gte=datetime.date.today()).order_by('event_date')
    name = request.user.profiles.name
    email = request.user.profiles.email
    bio = request.user.profiles.bio
    following = request.user.profiles.following.all()
    following_list = request.user.profiles.following.all()[:3]

    events_following = []
    following_events_sorted = None

    for user in following:
        user = User.objects.get(username=user)
        user_events = Event.objects.filter(user=user).filter(event_date__gte=datetime.date.today())
        events_following.append(user_events)

    following_events_sorted = sorted(chain(*events_following), key=lambda obj: obj.event_date)

    context = {
        'name': name,
        'email': email, 
        'bio': bio, 
        'events_now': events_now,
        'events_following': following_events_sorted,
        'following': following,
        'following_list': following_list,
        }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='accounts:login')
def followingList(request):
    following = request.user.profiles.following.all()
    context = {'following': following}
    return render(request, 'accounts/following.html', context)


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
    my_profile = Profiles.objects.get(user_id=request.user)

    if request.method == 'POST':
        if user_profile.user in my_profile.following.all():
            my_profile.following.remove(user_profile.user)
        else:
            my_profile.following.add(user_profile.user)

    if user_profile.user in my_profile.following.all():
        follow = True
    else:
        follow = False

    context = {
        'user': user_id,
        'user_events': user_events,
        'user_profile': user_profile,
        'follow': follow
        }
    return render(request, 'accounts/detail.html', context)
