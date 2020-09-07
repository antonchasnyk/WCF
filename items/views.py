from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
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


def search(queryset, request):
    q = request.GET.get('q', default='')
    item_list = queryset
    if q:
        chunks = q.split(' ')
        for chunk in chunks:
            item_list = item_list.filter(Q(part_number__icontains=chunk) |
                                         Q(comment__icontains=chunk) |
                                         Q(subcategory__name__icontains=chunk) |
                                         Q(subcategory__category__name__icontains=chunk)
                                         )
    paginator = Paginator(item_list, settings.ITEMS_ON_PAGE)
    page_number = request.GET.get('p')
    page_obj = paginator.get_page(page_number)
    if request.is_ajax():
        return True, render(request, 'items/ajax_search.html',
                      {'item_list': page_obj,
                       })
    else:
        return False, q, page_obj


@login_required(login_url=reverse_lazy('account:login'))
def components(request):
    item_list = Item.components.all()
    ajax, *z = search(item_list, request)

    if ajax:
        return z[0]
    else:
        q, page_obj = z
        return render(request,
                      'items/index.html',
                      {'item_list': page_obj,
                       'title': _('Components'),
                       'add_url': reverse_lazy('items:add_component'),
                       'q': q,
                       }
                      )


@login_required(login_url=reverse_lazy('account:login'))
def assembly_pars(request):
    item_list = Item.assembly_parts.all()

    ajax, *z = search(item_list, request)
    if ajax:
        return z[0]
    else:
        q, page_obj = z
        return render(request,
                      'items/index.html',
                      {'item_list': page_obj,
                       'title': _('Assembly parts'),
                       'add_url': reverse_lazy('items:add_assembly'),
                       }
                      )


@login_required(login_url=reverse_lazy('account:login'))
def consumables(request):
    item_list = Item.consumable.all()
    ajax, *z = search(item_list, request)
    if ajax:
        return z[0]
    else:
        q, page_obj = z
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
            messages.success(request, _('Item {} added ').format(item.designator()))
            return redirect(item.get_absolute_url())
        else:
            messages.error(request, _('Input incorrect. Check form fields'))
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


@login_required(login_url=reverse_lazy('account:login'))
def component(request, component_id):
    item = get_object_or_404(Item, pk=component_id)
    documents = item.document.all().prefetch_related('doc_type')
    if item.item_type == 'cm':
        title = _('Consumable Detail')
    else:
        title = _('Component Detail')
    return render(
        request,
        'items/detail_component.html',
        {'item': item,
         'title': title,
         'documents': documents,
         }
    )


@login_required(login_url=reverse_lazy('account:login'))
def assembly(request, assembly_id):
    item = get_object_or_404(Item, pk=assembly_id)
    documents = item.document.all().prefetch_related('doc_type')
    components = item.consist_of.filter(item__item_type='co').order_by('position')
    assemblies = item.consist_of.filter(item__item_type='ap').order_by('position')
    consumables = item.consist_of.filter(item__item_type='cm').order_by('position')
    if item.item_type == 'ap':
        title = _('Assembly Detail')
    else:
        title = _('Component Detail')
    return render(
        request,
        'items/detail_assembly.html',
        {'item': item,
         'title': title,
         'documents': documents,
         'components': components,
         'assemblies': assemblies,
         'consumables': consumables,
         }
    )
