from django_filters import FilterSet, CharFilter, DateFilter
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
                     'title': ['icontains'],
                     'publish': ['gte'],
                     'author': ['exact'],
                     'category': ['exact'],
        }