from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

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
                  'items/components.html',
                  {'components': item_list}
                  )


@login_required(login_url=reverse_lazy('account:login'))
def assembly_pars(request):
    item_list = Item.objects.filter(item_type='ap')
    return render(request,
                  'items/components.html',
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

