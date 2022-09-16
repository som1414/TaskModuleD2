from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import Post, Category, Author
from .filters import NewFilter
from .forms import NewForm
from django.core.paginator import Paginator

class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-dateCreation']
    paginate_by = 10

class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

class NewFilters(NewsList):
    template_name = "search.html"
    context_object_name = "search"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewFilter(self.request.GET, queryset=self.get_queryset())
        get_copy = self.request.GET.copy()
        if get_copy.get('page'):
            get_copy.pop('page')
        context['get_copy'] = get_copy
        return context


class NewCreate(CreateView):
    template_name = 'new_create.html'
    form_class = NewForm

class NewUpdate(UpdateView):
    template_name = 'new_create.html'
    form_class = NewForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class NewDelete(DeleteView):
    template_name = 'new_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
