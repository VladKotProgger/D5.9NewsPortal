from django import forms
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.forms import Textarea, ModelChoiceField

from NewsPaper.settings import DEFAULT_FROM_EMAIL
from .models import Post, Category, Author
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class ArticleNewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'post_author',
            'post_category',
            'topic',
            'text'
        ]


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        send_mail(
            subject=user.username,
            message='Вы успешно зарегистрировались',
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=[user.email]
        )
        return user
