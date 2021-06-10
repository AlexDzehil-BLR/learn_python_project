from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import CreateView

from .forms import AuthUserForm, RegisterProfilesForm


class ProfilesLogInView(LoginView):
    template_name = 'login.html'
    form_class = AuthUserForm
    success_url = reverse_lazy('index')


class RegisterProfilesView(CreateView):
    model = User
    template_name = 'registration/register.html'
    form_class = RegisterProfilesForm
    success_url = reverse_lazy('polls/log')

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class ProfilesLogout(LogoutView):
    next_page = reverse_lazy('index')




