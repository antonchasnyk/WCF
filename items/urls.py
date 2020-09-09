from django.urls import path

from . import views

app_name = 'items'

urlpatterns = [
    path('dashboard', views.index, name='dashboard'),
    path('components', views.components, name='component_list'),
    path('assemblies', views.assembly_pars, name='assembly_parts'),
    path('consumables', views.consumables, name='consumables'),
    path('items/search', views.context_search, name='context_search'),
    path('items/delete/<int:item_id>', views.delete_item, name='delete_item'),
    path('items/delete/doc/<int:doc_id>', views.delete_file, name='delete_file'),


    path('component/add', views.add_component, {'comp_type': 'co'}, name='add_component'),
    path('component/edit/<int:component_id>', views.edit_component, {'comp_type': 'co'}, name='edit_component'),
    path('component/<int:component_id>', views.component, name='detail_component'),

    path('assembly/add', views.add_component, {'comp_type': 'ap'}, name='add_assembly'),
    path('assembly/edit/<int:component_id>', views.add_component, {'comp_type': 'ap'}, name='edit_assembly'),
    path('assembly/<int:assembly_id>', views.assembly, name='detail_assembly'),

    path('consumable/add', views.add_component, {'comp_type': 'cm'}, name='add_consumable'),
    path('consumable/edit/<int:component_id>', views.edit_component, {'comp_type': 'cm'}, name='edit_consumable'),
    path('consumable/<int:component_id>', views.component, name='detail_consumable'),

    path('components/subcategory/add/<str:to>', views.subcategory_popup, name='subcategory_add_popup'),
    path('components/subcategory/<int:subcategory_id>/<str:to>', views.subcategory_popup,
         name='subcategory_edit_popup'),
    path('components/category/add/<str:to>', views.category_popup, name='category_add_popup'),
    path('components/category/<int:category_id>/<str:to>', views.category_popup, name='category_edit_popup'),
]