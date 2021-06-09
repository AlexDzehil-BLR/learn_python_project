from django.urls import path, include

from . import views

app_name = 'profiles'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', views.ProfilesLogInView.as_view(), name='login_page'),
    path('register/', views.RegisterProfilesView.as_view(), name='register'),
    path('logout/', views.ProfilesLogout.as_view(), name='logout_page'),
    path('<int:pk>', views.ProfilesLogout.as_view(), name='logout_page'),
]
