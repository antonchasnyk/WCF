from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from purchase.forms import ItemSelectableSearch
from purchase.models import ItemValue


@login_required(login_url=reverse_lazy('account:login'))
def needs(request):
    item_list = ItemValue.objects_needs.all()
    form = ItemSelectableSearch(request.GET)
    return render(request,
                  'purchase/needs.html',
                  {'item_list': item_list,
                   'title': _('Needs'),
                   'form': form,
                   }
                  )


@login_required(login_url=reverse_lazy('account:login'))
def in_progress(request):
    item_list = ItemValue.objects_in_progress.all()
    return render(request,
                  'purchase/in_progres.html',
                  {'item_list': item_list,
                   'title': _('In progress'),
                   }
                  )


@login_required(login_url=reverse_lazy('account:login'))
def done(request):
    item_list = ItemValue.objects_done.all()
    return render(request,
                  'purchase/done.html',
                  {'item_list': item_list,
                   'title': _('Done'),
                   }
                  )
