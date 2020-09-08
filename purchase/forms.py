from django import forms
from django.urls import reverse_lazy

from helpers.widgets import SelectableSearch


class ItemSelectableSearch(forms.Form):
    search = forms.CharField(widget=SelectableSearch(search_url=reverse_lazy('items:context_search')))
