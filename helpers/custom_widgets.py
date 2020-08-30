from django.forms.widgets import TextInput


class EmailInput(TextInput):
    input_type = 'email'


class PhoneInput(TextInput):
    input_type = 'tel'

