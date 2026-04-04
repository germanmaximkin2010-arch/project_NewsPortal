import django_filters
from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateFilter
from .models import Post, Author
from django.forms.widgets import DateInput


class PostFilter(FilterSet):
    author = ModelChoiceFilter(field_name='author', queryset=Author.objects.all(), label='Автор', empty_label='Все авторы')
    title = CharFilter(label='Содержание', lookup_expr='iregex')
    created_at = DateFilter(
        field_name='created_at',
        label='Дата создания после',
        lookup_expr='gte',
        widget=DateInput(
            attrs={'type': 'date'}
        )
    )
