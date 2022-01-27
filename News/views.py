from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Post, Category
from datetime import datetime


class PostList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-publish']
    paginate_by = 10
    queryset = Post.objects.order_by('-publish')


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()