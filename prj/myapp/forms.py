from django.forms import ModelForm, BooleanField
from .models import Post, Category, Author


class NewForm(ModelForm):
    check_box = BooleanField(label='Согласен!')

    class Meta:
        model = Post
        fields = ['author', 'categorySort', 'postCategory', 'rating']