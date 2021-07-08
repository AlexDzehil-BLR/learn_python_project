from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.event_list, name='index'),
    path('create_event/', views.create_event, name='create_event'),
    path('edit_event/<int:event_id>', views.edit_event, name='edit_event'),
    path('delete_event/<int:event_id>', views.delete_event, name='delete_event'),
]
