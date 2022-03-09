from django.shortcuts import render, redirect, reverse
from datetime import datetime
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, View, CreateView, DeleteView
from .models import *
from .filters import PostFilter
from django.core.paginator import Paginator
from .forms import PostForm
from .tasks import email_task
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 1
    queryset = Post.objects.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts_search'
    ordering = ['-publish']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()


class FilterPostView(ListView):
    model = Post
    template_name = 'posts_filter.html'
    context_object_name = 'posts_filter'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(CreateView, PermissionRequiredMixin):
    template_name = 'news_create.html'
    permission_required = ('news_create.html')
    form_class = PostForm


class PostUpdateView(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    template_name = 'news_create.html'
    form_class = PostForm
    login_required = ('news_update`')
    permission_required = ('news_update`')

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class IndexView(View):
    def get(self, request):
        # printer.delay(10)
        # printer.apply_async([10], countdown=5)
        # printer.apply_async([10], eta=datetime.now() + timedelta(seconds=5))
        # hello.delay()
        return redirect('/post/')

    class MyView(PermissionRequiredMixin, View):
        permission_required = ('<app>.<action>_<model>',
                               '<app>.<action>_<model>')


@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/news/categories')


@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'удален из подписчиков категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.remove(request.user)
    return redirect('/news/categories')


def sending_emails_to_subscribers(instance):
    sub_text = instance.text
    sub_title = instance.title

    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).post_category.pk)
    subscribers = category.subscribers.all()

    for subscriber in subscribers:
        subscriber_username = subscriber.username
        subscriber_useremail = subscriber.email
        html_content = render_to_string('news/mail.html',
                                        {'user': subscriber,
                                         'title': sub_title,
                                         'text': sub_text[:50],
                                         'post': instance})
        email_task(subscriber_username, subscriber_useremail, html_content)
    return redirect('/news/')