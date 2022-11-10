from django.urls import path

from . import views

app_name = 'conciertos'
urlpatterns = [
    path('', views.songs_artists, name='index'),
    path('songs_artists', views.songs_artists, name='songs_artists'),
    path('userinfo', views.userinfo, name='userinfo'),
    path('log_in', views.login_spotify, name='login_spotify'),
]