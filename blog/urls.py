from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView

urlpatterns = [
    path('api/blog/', PostListView.as_view(), name='post-list'),
    path('api/blog/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('api/blog/create/', PostCreateView.as_view(), name='post-create'),
]
