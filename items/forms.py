from django import forms
from django.forms import IntegerField, modelformset_factory
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _

from helpers.widgets import SelectableSearch
from items.models import ItemCategory, ItemDocFile, DocType, BOM
from .models import Item, ItemSubCategory


class ComponentForm(forms.ModelForm):
    value = IntegerField(min_value=0, required=False, label=_('In stock'))

    class Meta:
        model = Item
        fields = ['part_number', 'comment', 'subcategory', 'value_units']


class FileAddForm(forms.ModelForm):
    class Meta:
        model = ItemDocFile
        fields = ['doc_type', 'document']

    def save(self, commit=True, item_id=False):
        self.instance.item_id = item_id
        return super(FileAddForm, self).save(commit=commit)


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemSubCategory
        fields = ['name', 'parent', 'category']

    def __init__(self, *args, **kwargs):
        super(SubCategoryForm, self).__init__(*args, **kwargs)
        self.fields['parent'].required = False


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ['name']


class FileTypeForm(forms.ModelForm):
    class Meta:
        model = DocType
        fields = ['name']


class BOMForm(forms.ModelForm):
    class Meta:
        model = BOM
        fields = ['position', 'item', 'quantity']


BOMFormSet = modelformset_factory(BOM, form=BOMForm,
                                  widgets={'item': SelectableSearch(search_url=reverse_lazy('items:context_search'),
                                                                    model=Item)}, extra=1)
