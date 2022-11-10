from django.urls import path

from . import views

app_name = 'usuarios'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('log_out/', views.log_out, name='log_out'),
    
  
]