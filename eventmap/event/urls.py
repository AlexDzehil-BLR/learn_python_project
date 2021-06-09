from django.urls import path

from . import views

app_name = 'event'
urlpatterns = [
    path('', views.EventList.as_view(), name='index'),
]