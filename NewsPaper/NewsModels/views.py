from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post
import datetime

class PostList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'post'


class OnePost(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'