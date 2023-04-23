from django.shortcuts import render, get_object_or_404
from .models import Post, Topic
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator


class HomeListView(ListView):
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    queryset: Post.objects.all()

    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()

        return context


class MyPostListView(ListView):
    model = Post
    template_name = 'post/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(MyPostListView, self).get_context_data(**kwargs)

        context['posts'] = Post.objects.filter(
            author=user).order_by('-date_posted')
        context['topics'] = Topic.objects.all()
        return context


class UserPostListView(ListView):
    model = Post
    template_name = 'post/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super(UserPostListView, self).get_context_data(**kwargs)

        context['posts'] = Post.objects.filter(
            author=user).order_by('-date_posted')
        context['topics'] = Topic.objects.all()
        return context


class TopicPostListView(ListView):
    model = Post
    template_name = 'post/topic_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        selected_topic = get_object_or_404(Topic, id=self.kwargs.get('pk'))
        return Post.objects.filter(topic=selected_topic).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        selected_topic = get_object_or_404(Topic, id=self.kwargs.get('pk'))
        context = super(TopicPostListView, self).get_context_data(**kwargs)

        context['posts'] = Post.objects.filter(
            topic=selected_topic).order_by('-date_posted')
        context['topics'] = Topic.objects.all()
        context['selected_topic'] = selected_topic
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post/form.html'
    fields = ['title', 'content', 'image', 'topic']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['status'] = 'create'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post/form.html'
    fields = ['title', 'content', 'image', 'topic']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(**kwargs)
        context['status'] = 'update'
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post/confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        return context
