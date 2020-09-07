from django.urls import path

from . import views

app_name = 'purchase'

urlpatterns = [
    path('needs', views.needs, name='needs'),
    path('in_progress', views.in_progress, name='in_progress'),
    path('done', views.done, name='done'),
]
