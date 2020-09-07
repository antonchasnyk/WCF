from django.conf import settings
from django.urls import reverse

MENU_STRUCT = {
    'dash': (reverse('items:dashboard'),),
    'comp': '/component',
    'comp_all': (reverse('items:component_list'),),
    'comp_nop': (),
    'asp': '/assembl',
    'asp_all': (reverse('items:assembly_parts'),),
    'asp_nop': (),
    'cons': '/consumable',
    'cons_all': (reverse('items:consumables'),),
    'cons_nop': (),
    'team_all': (),
    'purch': '/purchase',
    'purch_needs': (reverse('purchase:needs'),),
    'purch_inp': (reverse('purchase:in_progress')),
    'purch_done': (reverse('purchase:done')),

}


def side_menu(request):
    kwargs = MENU_STRUCT.copy()
    for key in kwargs:
        if request.path.startswith(MENU_STRUCT[key]):
            kwargs[key] = 'active'
        else:
            kwargs[key] = ''
    return kwargs
