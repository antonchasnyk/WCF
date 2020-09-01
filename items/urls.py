from django.urls import path

from . import views

app_name = 'items'

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('components', views.components, name='component_list'),
    path('assemblies', views.assembly_pars, name='assembly_parts'),
    path('consumables', views.consumables, name='consumables'),
    path('bom/<int:number>', views.bom, name='bom_list'),

    path('component/add', views.edit_component, {'comp_type': 'co'}, name='add_components'),
    path('component/edit/<int:component_id>', views.edit_component, {'comp_type': 'co'}, name='edit_components'),

    path('assemblie/add', views.edit_component, {'comp_type': 'ap'}, name='add_assemblies'),
    path('assemblie/edit/<int:component_id>', views.edit_component, {'comp_type': 'ap'}, name='edit_assemblies'),

    path('consumable/add', views.edit_component, {'comp_type': 'cm'}, name='add_consumable'),
    path('consumable/edit/<int:component_id>', views.edit_component, {'comp_type': 'cm'}, name='edit_consumable'),

    path('components/subcategory/add/<str:to>', views.subcategory_popup, name='subcategory_add_popup'),
    path('components/subcategory/<int:subcategory_id>/<str:to>', views.subcategory_popup,
         name='subcategory_edit_popup'),
    path('components/category/add/<str:to>', views.category_popup, name='category_add_popup'),
    path('components/category/<int:category_id>/<str:to>', views.category_popup, name='category_edit_popup'),
]