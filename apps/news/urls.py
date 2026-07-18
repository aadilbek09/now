from django.urls import path

from .views import (
    AdminPostCreateView,
    AdminPostDetailView,
    PostDetailView,
    PostLatestView,
    PostListView,
)

urlpatterns = [
    # "latest" ni "<int:id>" dan OLDIN yozish shart.
    path('posts/latest', PostLatestView.as_view(), name='post-latest'),
    path('posts', PostListView.as_view(), name='post-list'),
    path('posts/<int:id>', PostDetailView.as_view(), name='post-detail'),
    path('admin/posts', AdminPostCreateView.as_view(), name='admin-post-create'),
    path('admin/posts/<int:id>', AdminPostDetailView.as_view(), name='admin-post-detail'),
]
