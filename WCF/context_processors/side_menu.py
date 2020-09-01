from django.conf import settings
from django.urls import reverse_lazy

MENU_STRUCT = {
    'dash': [reverse_lazy('items:dashboard')],
    'comp': [reverse_lazy('items:component_list')],
    'comp_all': [reverse_lazy('items:component_list')],
    'comp_nop': [],
    'asp': [reverse_lazy('items:assembly_parts')],
    'asp_all': [reverse_lazy('items:assembly_parts')],
    'asp_nop': [],
    'cons': [reverse_lazy('items:consumables')],
    'cons_all': [reverse_lazy('items:consumables')],
    'cons_nop': [],
    'team_all': [],

}


def side_menu(request):
    kwargs = MENU_STRUCT.copy()
    for key in kwargs:
        if request.path in MENU_STRUCT[key]:
            kwargs[key] = 'active'
        else:
            kwargs[key] = ''
    return kwargs
