from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea, ModelChoiceField

from .models import Post, Category, Author


class ArticleNewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_category',
            'topic',
            'text'
        ]

