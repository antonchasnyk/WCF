from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('login', views.log_in, name='component_list'),
]