import django_filters
from django.forms import DateInput
from django_filters import FilterSet, DateFilter, CharFilter, ModelChoiceFilter
from .models import *


class PostFilter(FilterSet):
    search_title = CharFilter(
        field_name='topic',
        label='Заголовок',
        lookup_expr='icontains'
    )

    search_author = ModelChoiceFilter(
        empty_label='Все авторы',
        field_name='post_author',
        label='Автор',
        queryset=Author.objects.all()
    )

    post_date = DateFilter(
        field_name='creation_time',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата',
        lookup_expr='date__gte'
    )
