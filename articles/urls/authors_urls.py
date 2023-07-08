from django.urls import path

from ..views.author_views import (
    AuthorCreateView,
    AuthorListView,
    AuthorUpdateView,
    AuthorDeleteView
)

urlpatterns = [
    path('create', AuthorCreateView.as_view(), name='author_create'),
    path('update/<int:pk>', AuthorUpdateView.as_view(), name='author_update'),
    path('list', AuthorListView.as_view(), name='author_list'),
    path('delete/<int:pk>', AuthorDeleteView.as_view(), name='author_delete'),
]