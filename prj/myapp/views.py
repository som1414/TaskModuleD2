from django.shortcuts import redirect, render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
from .models import Post, Category, Author
from .filters import NewFilter
from .forms import NewForm  # ,BaseRegisterForm
# from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime, date
from django.http import request, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-dateCreation']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        # context['time_now'] = datetime.utcnow()
        # context['count_posts'] = self.model.objects.filter(dateCreation__date=date.today(),
        #                                                    author__authUser__username=self.request.user).count()
        return context


class NewDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for cat in context['new'].postCategory.all():
            c = Category.objects.get(id=cat.id)
            context['is_not_subscribed'] = not c.subscribers.filter(username=self.request.user.username).exists()
        return context


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


class NewCreate(PermissionRequiredMixin, CreateView):
    template_name = 'new_create.html'
    form_class = NewForm
    permission_required = ('myapp.add_post',)

    def post(self, request, *args, **kwargs):
        form = NewForm(request.POST)
        post_category_pk = request.POST['postCategory']
        sub_text = request.POST.get('text')
        sub_title = request.POST.get('title')
        post_category = Category.objects.get(pk=post_category_pk)
        subscribers = post_category.subscribers.all()
        host = request.META.get('HTTP_HOST')

        # валидатор - чтоб данные в форме были корректно введены, без вредоносного кода от хакеров и прочего
        if form.is_valid():
            news = form.save(commit=False)
            news.save()

        for subscriber in subscribers:
            html_content = render_to_string(
                'send_create.html',
                {'user': subscriber, 'text': sub_text[:50], 'post': news, 'title': sub_title, 'host': host}
            )

            msg = EmailMultiAlternatives(
                subject=f'{sub_title}',
                body=f'Здравствуй, {subscriber.username}! Новая статья в вашем любимом разделе! {sub_text[:50]}',
                from_email='som1414@yandex.ru',
                to=[subscriber.email],
            )

            msg.attach_alternative(html_content, "text/html")
            msg.send()
        return redirect('/news/')


class NewUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'new_create.html'
    form_class = NewForm
    permission_required = ('myapp.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'new_delete.html'
    queryset = Post.objects.all()
    permission_required = ('myapp.delete_post',)
    success_url = '/news/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/news')

class CategoryList(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'categories'

class CategoryDetail(DetailView):
    template_name = 'category_subscription.html'
    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category_subscribers = Category.objects.filter(pk=category_id).values("subscribers__username")
        context['is_not_subscribe'] = not category_subscribers.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = category_subscribers.filter(subscribers__username=self.request.user).exists()
        return context

@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/categories')

@login_required
def del_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/categories')

# class BaseRegisterView(CreateView):
#     model = User
#     form_class = BaseRegisterForm
#     success_url = '/'
