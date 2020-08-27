from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('account/profile', views.profile_detail, name='profile_detail'),
]
