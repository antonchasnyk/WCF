from django import forms
from django.utils.translation import ugettext_lazy as _

from items.models import ItemCategory
from .models import Item, ItemSubCategory


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['part_number', 'comment', 'subcategory', 'value', 'value_units']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemSubCategory
        fields = ['name', 'category']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ['name']
