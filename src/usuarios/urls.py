from django.urls import path

from . import views

app_name = 'usuarios'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('log_out/', views.log_out, name='log_out'),
    path('OTP_verify/', views.introducir_token, name='OTP_verify'),
    path('success', views.verified, name='verified')
]