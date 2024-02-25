from os import name
from django.urls import path
from .views import (PostCreateView, PostDetailView, PostListView, PostUpdateView, PostDeleteView, UserPostListView)
from . import views


urlpatterns = [ 
            
            path('login/', views.loginView, name="login"),
            path('logout/', views.LogoutView, name="logout"),
            path('register/', views.registerUser, name="register"),
            path('search/', views.search, name="search"),
            path('', PostListView.as_view(), name="home"),
            path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
            path('post-create/', PostCreateView.as_view(), name='post-create'),
            path('post-detail/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
            path('post-update/<int:pk>/', PostUpdateView.as_view(), name='post-update'),
            path('post-delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
]