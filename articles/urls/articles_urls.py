from django.urls import path
from ..views.articles_view import (
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
)

from ..views.comment_views import (
    CommentCreateView, 
    CommentUpdateView, 
    CommentDeleteView
)

urlpatterns = [
    path('create', ArticleCreateView.as_view(), name='article_create'),
    path('list', ArticleListView.as_view(), name='article_list'),
    path('detail/<int:pk>', ArticleDetailView.as_view(), name='article_detail'),
    path('update/<int:pk>', ArticleUpdateView.as_view(), name='article_update'),
    path('delete/<int:pk>', ArticleDeleteView.as_view(), name='article_delete'),
    
    path('detail/<int:pk>/comments/add', CommentCreateView.as_view(), name='add_comment'),
    path('detail/<int:pk>/comments/update', CommentUpdateView.as_view(), name='update_comment'),
    path('detail/<int:pk>/comments/delete', CommentDeleteView.as_view(), name='delete_comment'),
]