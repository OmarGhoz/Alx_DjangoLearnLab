from django import forms
from django.contrib.auth.models import User
from .models import Post
from .models import Comment
from taggit.forms import TagField

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'title', 'content']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }

class PostForm(forms.ModelForm):
    tags = TagField(required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']