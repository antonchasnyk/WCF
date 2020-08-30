from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from account.models import Profile
from helpers.custom_widgets import PhoneInput


class LoginForm(forms.Form):
    name = forms.CharField(label=_('Login'), max_length=20)
    password = forms.CharField(label=_('Password'), max_length=20, widget=forms.PasswordInput())


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }

    def clean_first_name(self):
        if self.cleaned_data['first_name'] == '':
            raise ValidationError(_('First Name is required'))
        return self.cleaned_data['first_name']

    def clean_last_name(self):
        if self.cleaned_data['last_name'] == '':
            raise ValidationError(_('Last Name is required'))
        return self.cleaned_data['last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile_phone', 'internal_phone', 'bio', 'location']
        labels = {
            'mobile_phone': _('Mobile Number'),
            'internal_phone': _('Internal Number'),
            'bio': _('Bio'),
            'location': _('Location'),
        }

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['mobile_phone'].widget = PhoneInput()
        self.fields['internal_phone'].widget = PhoneInput()
