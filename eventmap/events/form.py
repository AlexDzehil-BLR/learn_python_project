from django import forms
from django.forms import ModelForm

from .models import Event


class CreateEventForm(ModelForm):
    event_date = forms.DateTimeField(input_formats=['%d.%m.%Y %H:%M'], label='Дата')

    class Meta:
        model = Event
        fields = '__all__'
        exclude = ['user']
        labels = {
            'title': 'Событие',
            'text': 'Описание',
            'location': 'Место',
            'type_of_event': 'Тип события',
        }

