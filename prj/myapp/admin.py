from django.contrib import admin
from .models import Category, Author, Post, PostCategory, Comment, Subscriber


def nullfy_rating(modeladmin, request, queryset):
    queryset.update(rating=0)


nullfy_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'dateCreation', 'categorySort', 'rating']
    list_filter = ('postCategory', 'dateCreation', 'title')
    search_fields = ('title', 'postCategory__designation')
    actions = [nullfy_rating]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Subscriber)
