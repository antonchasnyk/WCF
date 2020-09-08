from django import forms

from helpers.widgets import SelectableSearch


class ItemSelectableSearch(forms.Form):
    search = forms.CharField(widget=SelectableSearch())
