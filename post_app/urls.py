from django.urls import path
from . import views
from .views import HomeListView, MyPostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, TopicPostListView, CommentCreateView, SavePostView, SavedPostListView, comments_list

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('mine', MyPostListView.as_view(), name='mine'),
    
    path('saved', SavedPostListView.as_view(), name='saved'),
    
    path('topic/<int:pk>/', TopicPostListView.as_view(), name='topic-posts'),
    
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    
    
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment-create'),
    
    path('comments/list/', comments_list, name='comments-list'),
    
    path('post/<int:post_id>/save/', SavePostView, name='post-save'),

    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('post/<int:pk>/upvote/', views.upvote, name='upvote'),
    path('post/<int:pk>/downvote/', views.downvote, name='downvote')
    
]
