from django import forms
from django.forms import IntegerField
from django.utils.translation import ugettext_lazy as _

from items.models import ItemCategory, ItemDocFile, DocType
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
        fields = ['name', 'category']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = ItemCategory
        fields = ['name']


class FileTypeForm(forms.ModelForm):
    class Meta:
        model = DocType
        fields = ['name']