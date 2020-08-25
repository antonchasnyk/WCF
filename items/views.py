from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Item, BOM


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
# Create your views here.


def components(request):
    item_list = Item.objects.filter(item_type='co')
    return render(request,
                  'components.html',
                  {'components': item_list}
                  )


def bom(request, number):
    item = get_object_or_404(Item, pk=number)
    item_list = item.assembly_part.all()
    return render(request,
                  'bom.html',
                  {
                    'items': item_list,
                    'assembly_part': item,
                  }
                  )

