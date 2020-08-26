from django.conf import settings
from django.urls import reverse_lazy

MENU_STRUCT = {
    'dash': [reverse_lazy('dashboard')],
    'comp': [reverse_lazy('component_list')],
    'comp_all': [reverse_lazy('component_list')],
    'comp_nop': [],
    'asp': [reverse_lazy('assembly_parts')],
    'asp_all': [reverse_lazy('assembly_parts')],
    'asp_nop': [],
    'cons': [],
    'cons_all': [],
    'cons_nop': [],
}


def side_menu(request):
    kwargs = MENU_STRUCT.copy()
    for key in kwargs:
        if request.path in MENU_STRUCT[key]:
            kwargs[key] = 'active'
        else:
            kwargs[key] = ''
    print(kwargs)
    print(MENU_STRUCT)
    return kwargs
