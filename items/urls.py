from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('components', views.components, name='component_list'),
    path('assemblies', views.assembly_pars, name='assembly_parts'),
    path('bom/<int:number>', views.bom, name='bom_list'),
]