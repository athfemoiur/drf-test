from django.urls import path

from post.api.views import PostListView, PostScoreView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:post_id>/score/', PostScoreView.as_view(), name='post-score')
]
