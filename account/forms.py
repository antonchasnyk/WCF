from django import forms
from django.utils.translation import ugettext as _


class LoginForm(forms.Form):
    name = forms.CharField(label=_('Login'), max_length=20)
    password = forms.CharField(label=_('Password'), max_length=20, widget=forms.PasswordInput())
