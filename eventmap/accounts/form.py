from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profiles


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfilesForm(ModelForm):
    class Meta:
        model = Profiles
        fields = '__all__'
        exclude = ['user', 'following']
