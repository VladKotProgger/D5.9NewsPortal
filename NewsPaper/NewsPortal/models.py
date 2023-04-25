from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.urls import reverse
from django import forms
from django.contrib.auth.models import User, Group


article = 'STA'
news = 'NOV'

article_or_news = [
    (article, "Статья"),
    (news, "Новость")
]


class Author(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1
    )
    author_rating = models.FloatField(default=0.0)

    def update_rating(self):
        all_posts = Post.objects.filter(post_author_id=self.user)
        post_rate = 0.0
        for post in all_posts:
            post_rate += post.post_rating * 3

        all_comments = Comment.objects.filter(comment_post_id=self.user)
        comment_rate = 0.0
        for comment in all_comments:
            comment_rate += comment.comment_rating

        self.author_rating = post_rate + comment_rate
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    subject = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.subject


class Post(models.Model):
    post_author = models.ForeignKey('Author', on_delete=models.CASCADE)
    article_news = models.CharField(max_length=3,
                                    choices=article_or_news,
                                    default=news)
    creation_time = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField('Category', through='PostCategory')
    topic = models.CharField(max_length=255)
    text = models.TextField(default='Текст статьи/новости')
    post_rating = models.FloatField(default=0.0)

    def like(self):
        self.post_rating += 1.0
        self.save()
        return self.post_rating

    def dislike(self):
        self.post_rating -= 1.0
        self.save()
        return self.post_rating

    def preview(self):
        if len(self.text) <= 124:
            return self.text
        else:
            return self.text[:124] + '...'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)


class Comment(models.Model):
    comment_post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating += 1.0
        self.save()
        return self.comment_rating

    def dislike(self):
        self.comment_rating -= 1.0
        self.save()
        return self.comment_rating


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)

    def save(self, *args, **kwargs):
        user = super(BaseRegisterForm, self).save(*args, **kwargs)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
