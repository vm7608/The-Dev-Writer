from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Topic, Comment, SavePost, Vote
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
# import reverse_lazy to use in class based views
from django.urls import reverse_lazy
# import django messages
from django.contrib import messages


class HomeListView(ListView):
    model = Post
    template_name = 'post/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    queryset: Post.objects.all()

    def get_context_data(self, **kwargs):

        # return posts by keyword
        if 'keyword' in self.request.GET:
            keyword = self.request.GET.get('keyword')
            context = super(HomeListView, self).get_context_data(**kwargs)
            context['posts'] = Post.objects.filter(
                title__icontains=keyword).order_by('-date_posted')
            context['topics'] = Topic.objects.all()
            messages.success(self.request, f"Search result of '{keyword}'")
            # Get user vote for each post 
            user_voted = {} 
            if self.request.user.is_authenticated :
                for post in context['posts'] : 
                    try : 
                        vote = Vote.objects.get(user=self.request.user, voted_post=post) 
                        user_voted[post.id] = vote.vote_type
                    except Vote.DoesNotExist : 
                        pass
            context['user_voted'] = user_voted
            return context

        context = super(HomeListView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
	
        # Get user vote for each post
        user_voted = {}
        if self.request.user.is_authenticated :
            for post in context['posts'] :
                try :
                    vote = Vote.objects.get(user=self.request.user, voted_post=post)
                    user_voted[post.id] = vote.vote_type
                except Vote.DoesNotExist :
                    pass
        context['user_voted'] = user_voted

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
        if 'keyword' in self.request.GET:
            keyword = self.request.GET.get('keyword')
            context = super(MyPostListView, self).get_context_data(**kwargs)
            context['posts'] = Post.objects.filter(
                title__icontains=keyword, author=user).order_by('-date_posted')
            context['topics'] = Topic.objects.all()
            messages.success(self.request, f"Search result of '{keyword}'")
            # Get user vote for each post 
            user_voted = {} 
            if self.request.user.is_authenticated :
                for post in context['posts'] : 
                    try : 
                        vote = Vote.objects.get(user=self.request.user, voted_post=post) 
                        user_voted[post.id] = vote.vote_type
                    except Vote.DoesNotExist : 
                        pass
            context['user_voted'] = user_voted

            return context

        context = super(MyPostListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            author=user).order_by('-date_posted')
        context['topics'] = Topic.objects.all()

        # Get user vote for each post 
        user_voted = {} 
        if self.request.user.is_authenticated :
            for post in context['posts'] : 
                try : 
                    vote = Vote.objects.get(user=self.request.user, voted_post=post) 
                    user_voted[post.id] = vote.vote_type
                except Vote.DoesNotExist : 
                    pass
        context['user_voted'] = user_voted

        return context

class SavedPostListView(ListView):
    model = SavePost
    template_name = 'post/saved_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        return SavePost.objects.filter(user=user).order_by('-date_saved')

    def get_context_data(self, **kwargs):
        user = self.request.user
        if 'keyword' in self.request.GET:
            keyword = self.request.GET.get('keyword')
            context = super(SavedPostListView, self).get_context_data(**kwargs)
            temp = SavePost.objects.filter(
                user=user, post__title__icontains=keyword).order_by('-date_saved')
            context['posts'] = [post.post for post in temp]
            context['topics'] = Topic.objects.all()
            messages.success(self.request, f"Search result of '{keyword}'")
            # Get user vote for each post 
            user_voted = {} 
            if self.request.user.is_authenticated :
                for post in context['posts'] : 
                    try : 
                        vote = Vote.objects.get(user=self.request.user, voted_post=post) 
                        user_voted[post.id] = vote.vote_type
                    except Vote.DoesNotExist : 
                        pass
            context['user_voted'] = user_voted
            return context

        context = super(SavedPostListView, self).get_context_data(**kwargs)
        temp = SavePost.objects.filter(user=user).order_by('-date_saved')
        context['posts'] = [post.post for post in temp]
        context['topics'] = Topic.objects.all()

        # Get user vote for each post 
        user_voted = {} 
        if self.request.user.is_authenticated :
            for post in context['posts'] : 
                try : 
                    vote = Vote.objects.get(user=self.request.user, voted_post=post) 
                    user_voted[post.id] = vote.vote_type
                except Vote.DoesNotExist : 
                    pass
        context['user_voted'] = user_voted
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
        
        if 'keyword' in self.request.GET:
            keyword = self.request.GET.get('keyword')
            
            context = super(UserPostListView, self).get_context_data(**kwargs)
            context['posts'] = Post.objects.filter(
                author=user, title__icontains=keyword).order_by('-date_posted')
            context['topics'] = Topic.objects.all()
            messages.success(self.request, f"Search result of '{keyword}'")
            # Get user vote for each post 
            user_voted = {} 
            if self.request.user.is_authenticated :
                for post in context['posts'] : 
                    try : 
                        vote = Vote.objects.get(user=self.request.user, voted_post=post) 
                        user_voted[post.id] = vote.vote_type
                    except Vote.DoesNotExist : 
                        pass
            context['user_voted'] = user_voted
            return context
        
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(
            author=user).order_by('-date_posted')
        context['topics'] = Topic.objects.all()

        # Get user vote for each post 
        user_voted = {} 
        if self.request.user.is_authenticated :
            for post in context['posts'] : 
                try : 
                    vote = Vote.objects.get(user=self.request.user, voted_post=post) 
                    user_voted[post.id] = vote.vote_type
                except Vote.DoesNotExist : 
                    pass
        context['user_voted'] = user_voted
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
        
        if 'keyword' in self.request.GET:
            keyword = self.request.GET.get('keyword')
            context = super(TopicPostListView, self).get_context_data(**kwargs)
            context['posts'] = Post.objects.filter(topic=selected_topic, title__icontains=keyword).order_by('-date_posted')
            context['topics'] = Topic.objects.all()
            context['selected_topic'] = selected_topic
            messages.success(self.request, f"Search result of '{keyword}'")
            # Get user vote for each post 
            user_voted = {} 
            if self.request.user.is_authenticated :
                for post in context['posts'] : 
                    try : 
                        vote = Vote.objects.get(user=self.request.user, voted_post=post) 
                        user_voted[post.id] = vote.vote_type
                    except Vote.DoesNotExist : 
                        pass
            context['user_voted'] = user_voted
            return context
        
        
        context = super(TopicPostListView, self).get_context_data(**kwargs)

        context['posts'] = Post.objects.filter(topic=selected_topic).order_by('-date_posted')
        context['topics'] = Topic.objects.all()
        context['selected_topic'] = selected_topic

        # Get user vote for each post 
        user_voted = {} 
        if self.request.user.is_authenticated :
            for post in context['posts'] : 
                try : 
                    vote = Vote.objects.get(user=self.request.user, voted_post=post) 
                    user_voted[post.id] = vote.vote_type
                except Vote.DoesNotExist : 
                    pass
        context['user_voted'] = user_voted
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post/detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['topics'] = Topic.objects.all()
        # context['comments'] = self.get_comments()

        user = self.request.user 
        post = context['post']
        user_voted = None 
        if user.is_authenticated : 
            try : 
                vote =  Vote.objects.get(user=user, voted_post=post) 
                user_voted = vote.vote_type 
            except Vote.DoesNotExist : 
                pass
        context['user_voted'] = user_voted
        return context

    def get_comments(self):
        post = self.get_object()
        return post.comments.all().order_by('-date_posted')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        post_pk = self.kwargs['pk']
        post = get_object_or_404(Post, pk=post_pk)
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post_pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': post_pk})

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context['status'] = 'create'
        return context


def comments_list(request):
    postid = request.GET.get('post')
    post = get_object_or_404(Post, id=postid)
    comments = Comment.objects.filter(post =post).order_by('-date_posted')
    context = {'comments': comments}
    return render(request, 'comment/comment.html', context)



def SavePostView(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    saved_post, created = SavePost.objects.get_or_create(
        post=post, user=request.user)
    if created:
        # Nếu đây là lần đầu tiên người dùng lưu bài viết này
        messages.success(request, f"Post '{post.title}' has been saved!")
    else:
        # Nếu người dùng đã lưu bài viết này trước đó
        saved_post.delete()
        messages.success(request, f"Post '{post.title}' has been unsaved!")
    return redirect('post-detail', pk=post_id)

# from django.core.management import call_command
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post/form.html'
    fields = ['title', 'content', 'image', 'topic']

    def form_valid(self, form):
        form.instance.author = self.request.user
        # call_command('collectstatic', interactive=False)
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

def upvote(request, pk) : 
    post = Post.objects.get(pk=pk) 
    vote, created = Vote.objects.get_or_create(user=request.user, voted_post=post)
    print("upvoted")
    if vote.vote_type == Vote.UPVOTE: 
        # User da upvote truoc do, xoa upvote va giam vote_count
        post.vote_count -= 1
        vote.delete() 
    else : 
        # User chua upvote hoac da upvote, thuc hien upvote va tang vote_count
        if vote.vote_type == Vote.DOWNVOTE : 
            post.vote_count += 1
        
        post.vote_count += 1
        vote.vote_type = Vote.UPVOTE
        vote.save() 

    post.save() 
    return JsonResponse({'vote-count': post.vote_count}) 

def downvote(request, pk) : 
    post = Post.objects.get(pk=pk) 
    vote, created = Vote.objects.get_or_create(user=request.user, voted_post=post)  
    print("downvoted")
    # print(vote.vote_type)
    if vote.vote_type == Vote.DOWNVOTE :
        # User da downvote truoc do, xoa downvote va tang vote_count
        post.vote_count += 1
        vote.delete() 
    else : 
        # User chua downvote hoac da upvote, thuc hien downvote va giam vote_count 
        if vote.vote_type == vote.UPVOTE : 
            # User da upvote truoc do, giam vote_count 
            post.vote_count -= 1 
        post.vote_count -= 1 
        vote.vote_type = vote.DOWNVOTE 
        vote.save() 
    
    post.save() 
    return JsonResponse({'vote-count': post.vote_count}) 