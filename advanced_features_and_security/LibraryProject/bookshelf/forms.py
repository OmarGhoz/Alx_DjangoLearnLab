from django import forms
from django.core.validators import validate_email

class UserForm(forms.Form):
    email = forms.EmailField(validators=[validate_email])
ExampleForm