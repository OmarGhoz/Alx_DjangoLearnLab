from django import forms
from django.contrib.auth.models import User
from .models import Post

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'title', 'content']
