from django.forms import ModelForm
from .models import Event


class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['user']
