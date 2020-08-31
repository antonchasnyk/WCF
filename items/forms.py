from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Item, ItemSubCategory


class ComponentForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['part_number', 'comment', 'subcategory', 'value', 'value_units']


class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = ItemSubCategory
        fields = ['name', 'category']

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name']
#         labels = {
#             'first_name': _('First Name'),
#             'last_name': _('Last Name'),
#         }
#
#     def clean_first_name(self):
#         if self.cleaned_data['first_name'] == '':
#             raise ValidationError(_('First Name is required'))
#         return self.cleaned_data['first_name']
#
#     def clean_last_name(self):
#         if self.cleaned_data['last_name'] == '':
#             raise ValidationError(_('Last Name is required'))
#         return self.cleaned_data['last_name']
#
#
# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['mobile_phone', 'internal_phone', 'bio', 'location']
#         labels = {
#             'mobile_phone': _('Mobile Number'),
#             'internal_phone': _('Internal Number'),
#             'bio': _('Bio'),
#             'location': _('Location'),
#         }
#
#     def __init__(self, *args, **kwargs):
#         super(ProfileForm, self).__init__(*args, **kwargs)
#         self.fields['mobile_phone'].widget = PhoneInput()
#         self.fields['internal_phone'].widget = PhoneInput()