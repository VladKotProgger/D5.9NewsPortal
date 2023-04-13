import django_filters
from django.forms import DateInput
from django_filters import FilterSet, DateFilter
from .models import Post


class PostFilter(FilterSet):
    creation_time = DateFilter(
        widget=DateInput(attrs={'type': 'date'}),
        label='Дата позже',
        lookup_expr='date__gt'
    )

    class Meta:
        model = Post
        fields = {
            'topic': ['icontains'],
            'post_author__user__username': ['icontains'],
        }
