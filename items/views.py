from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from .forms import ComponentAddForm
from .models import Item, BOM


@login_required(login_url=reverse_lazy('account:login'))
def index(request):
    return render(request,
                  'index.html',
                  {}
                  )
# Create your views here.


@login_required(login_url=reverse_lazy('account:login'))
def components(request):
    item_list = Item.objects.filter(item_type='co')
    return render(request,
                  'items/index.html',
                  {'components': item_list}
                  )


@login_required(login_url=reverse_lazy('account:login'))
def assembly_pars(request):
    item_list = Item.objects.filter(item_type='ap')
    return render(request,
                  'items/index.html',
                  {'components': item_list}
                  )


@login_required(login_url=reverse_lazy('account:login'))
def bom(request, number):
    item = get_object_or_404(Item, pk=number)
    item_list = item.assembly_part.all()
    return render(request,
                  'items/bom.html',
                  {
                    'items': item_list,
                    'assembly_part': item,
                  }
                  )


@login_required(login_url=reverse_lazy('account:login'))
@permission_required('items.add_item', raise_exception=PermissionDenied())
def edit_component(request, component_id=-1):
    if component_id >= 0:
        item = get_object_or_404(Item, pk=component_id)
    else:
        item = None
    if request.method == 'POST':
        item_form = ComponentAddForm(request.POST, instance=item)
        if item_form.is_valid():
            item_form.instance.created_by = request.user
            item_form.instance.item_type = 'co'
            item_form.save()
            return redirect("items:component_list")
        else:
            messages.error(request, _('Input incorrect'), extra_tags='alert-danger')
    else:
        item_form = ComponentAddForm(instance=item)
    return render(
        request,
        'items/edit_component.html',
        {'item_form': item_form,
         }
    )
