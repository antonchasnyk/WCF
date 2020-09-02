from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _

from WCF import settings
from items.forms import CategoryForm
from items.models import ItemCategory
from purchase.models import ItemValue
from .forms import ComponentForm, SubCategoryForm
from .models import Item, BOM, ItemSubCategory


@login_required(login_url=reverse_lazy('account:login'))
def index(request):
    return render(request,
                  'index.html',
                  {}
                  )


@login_required(login_url=reverse_lazy('account:login'))
def components(request):
    item_list = Item.components.all()
    paginator = Paginator(item_list, settings.ITEMS_ON_PAGE)
    page_number = request.GET.get('p')
    page_obj = paginator.get_page(page_number)
    return render(request,
                  'items/index.html',
                  {'item_list': page_obj,
                   'title': _('Components'),
                   'add_url': reverse_lazy('items:add_components'),
                   }
                  )


@login_required(login_url=reverse_lazy('account:login'))
def assembly_pars(request):
    item_list = Item.assembly_parts.all()
    paginator = Paginator(item_list, settings.ITEMS_ON_PAGE)
    page_number = request.GET.get('p')
    page_obj = paginator.get_page(page_number)
    return render(request,
                  'items/index.html',
                  {'item_list': page_obj,
                   'title': _('Assembly parts'),
                   'add_url': reverse_lazy('items:add_assemblies'),
                   }
                  )


@login_required(login_url=reverse_lazy('account:login'))
def consumables(request):
    item_list = Item.consumable.all()
    paginator = Paginator(item_list, settings.ITEMS_ON_PAGE)
    page_number = request.GET.get('p')
    page_obj = paginator.get_page(page_number)
    return render(request,
                  'items/index.html',
                  {'item_list': page_obj,
                   'title': _('Consumables'),
                   'add_url': reverse_lazy('items:add_consumable'),
                   }
                  )


@login_required(login_url=reverse_lazy('account:login'))
def bom(request, number):
    item = get_object_or_404(Item, pk=number)
    item_list = item.consist_of.order_by('item__subcategory__category', 'position').all()
    print(item_list)
    return render(request,
                  'items/bom.html',
                  {
                    'item_list': item_list,
                    'assembly_part': item,
                  }
                  )


@login_required(login_url=reverse_lazy('account:login'))
@permission_required('items.add_item', raise_exception=PermissionDenied())
@transaction.atomic
def edit_component(request, comp_type, component_id=-1):
    if component_id >= 0:
        item = get_object_or_404(Item, pk=component_id)
    else:
        item = None
    if request.method == 'POST':
        item_form = ComponentForm(request.POST, instance=item)
        if item_form.is_valid():
            item_form.instance.created_by = request.user
            item_form.instance.item_type = comp_type
            item = item_form.save()
            if item_form.cleaned_data['value'] > 0:
                value = ItemValue(value=item_form.cleaned_data['value'],
                                  created_by=request.user,
                                  item=item)
                value.save()
            if comp_type == 'co':
                return redirect("items:component_list")
            elif comp_type == 'ap':
                return redirect("items:assembly_parts")
            elif comp_type == 'cm':
                return redirect("items:consumables")
        else:
            messages.error(request, _('Input incorrect'), extra_tags='alert-danger')
    else:
        item_form = ComponentForm(instance=item)

    if comp_type == 'co':
        title = _('Edit Component')
    elif comp_type == 'ap':
        title = _('Edit Assembly Part')
    elif comp_type == 'cm':
        title = _('Edit Consumable')
    else:
        title = _('Unknown Type')
    return render(
        request,
        'items/edit_component.html',
        {'item_form': item_form,
         'title': title,
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

