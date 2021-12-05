from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from post.api.serializers import PostSerializer, PostScoreSerializer
from post.models import Post
from rest_framework.exceptions import NotFound


class PostListView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostScoreView(CreateAPIView):
    serializer_class = PostScoreSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            post = Post.objects.get(id=self.kwargs['post_id'])
        except Post.DoesNotExist:
            raise NotFound
        return post

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user, post=self.get_object())
