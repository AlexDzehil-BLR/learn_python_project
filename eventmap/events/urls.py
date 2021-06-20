from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.event_list, name='index'),
    path('create_event/', views.create_event, name='create_event')
]
