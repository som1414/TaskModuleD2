from django_filters import FilterSet
from .models import Post  # ,Category, Author


class NewFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'author__authUser__username': ['icontains'],
            'title': ['icontains'],
            'dateCreation': ['gt'],
        }
