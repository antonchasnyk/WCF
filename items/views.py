from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from items.forms import CategoryForm
from items.models import ItemCategory
from .forms import ComponentForm, SubCategoryForm
from .models import Item, BOM, ItemSubCategory


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
        item_form = ComponentForm(request.POST, instance=item)
        if item_form.is_valid():
            item_form.instance.created_by = request.user
            item_form.instance.item_type = 'co'
            item_form.save()
            return redirect("items:component_list")
        else:
            messages.error(request, _('Input incorrect'), extra_tags='alert-danger')
    else:
        item_form = ComponentForm(instance=item)
    return render(
        request,
        'items/edit_component.html',
        {'item_form': item_form,
         }
    )


@login_required(login_url=reverse_lazy('account:login'))
@permission_required('items.add_item', raise_exception=PermissionDenied())
def subcategory_popup(request, to, subcategory_id=-1):
    if subcategory_id >= 0:
        subcategory = get_object_or_404(ItemSubCategory, id=subcategory_id)
    else:
        subcategory = None
    form = SubCategoryForm(request.POST or None, instance=subcategory)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#%s");</script>' % (instance.pk, instance, to))
    return render(request, "items/edit_subcategory_popup.html", {"form": form})


@login_required(login_url=reverse_lazy('account:login'))
@permission_required('items.add_item', raise_exception=PermissionDenied())
def category_popup(request, to, category_id=-1):
    if category_id >= 0:
        category = get_object_or_404(ItemCategory, id=category_id)
    else:
        category = None
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        instance = form.save()
        return HttpResponse(
            '<script>opener.closePopup(window, "%s", "%s", "#%s");</script>' % (instance.pk, instance, to))
    return render(request, "items/edit_category_popup.html", {"form": form})

