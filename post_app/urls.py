from django.urls import path
from . import views
from .views import HomeListView, MyPostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView, TopicPostListView

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('mine', MyPostListView.as_view(), name='mine'),
    path('topic/<int:pk>', TopicPostListView.as_view(), name='topic-posts'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/create/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
]
