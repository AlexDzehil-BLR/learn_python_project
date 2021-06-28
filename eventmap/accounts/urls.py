from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),
    path('settings/', views.profileSettings, name='settings'),
    path('profile/', views.profilePage, name='profile'),
    path('profiles_all/', views.ProfilesAll.as_view(), name='profiles_all'),
    path('detail/<int:pk>', views.user_detail_view, name='detail')
]
