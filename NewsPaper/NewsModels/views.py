from django.views.generic import *
from .filters import PostFilter
from .models import *
from django.shortcuts import render, redirect
from django_filters.views import FilterView
from .forms import *
from django.urls import reverse_lazy

class PostList(FilterView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'post'
    paginate_by = 10
    filterset_class = PostFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        post_filtered = PostFilter(self.request.GET, queryset=queryset)
        return post_filtered.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


def post_list(request):
    posts = Post.objects.all()

    if request.GET.get('title') is not None:
        title = request.GET.get('title')
        posts_filtered = posts.filter(title__iregex=title).order_by('-created_at')
        return render(request, 'posts.html', {'posts': posts_filtered})

    return render(request, 'posts.html', {'posts': posts})


class OnePost(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(CreateView):
    model = Post
    template_name = 'post_create.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit = False)
        if 'news' in self.request.path:
            post.type = 'NW'
        post.save()
        return super().form_valid(form)


class PostUpdate(UpdateView):
    model = Post
    template_name = 'post_update.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit = False)
        if 'news' in self.request.path:
            post.type = 'NW'
        post.save()
        return super().form_valid(form)


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def post_delete(self):
        post = self.get_object()
        post.delete()

def __init__():
    pass