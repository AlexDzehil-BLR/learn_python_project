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
    template_name = 'register.html'
    form_class = RegisterProfilesForm
    success_url = None

    def get_success_url(self):
        return 'admin/'


class ProfilesLogout(LogoutView):
    next_page = reverse_lazy('index')



