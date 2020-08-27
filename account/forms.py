from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from account.models import Profile


class LoginForm(forms.Form):
    name = forms.CharField(label=_('Login'), max_length=20)
    password = forms.CharField(label=_('Password'), max_length=20, widget=forms.PasswordInput())


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['mobile_phone', 'internal_phone', 'bio', 'location']
