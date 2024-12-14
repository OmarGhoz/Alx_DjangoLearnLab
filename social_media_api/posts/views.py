from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_feed(request):
    followed_users = request.user.following.all()
    posts = Post.objects.filter(author__in=followed_users).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

class FeedView(APIView):
    """
    Generates a feed of posts from users the current user follows.
    Returns posts ordered by creation date, with the most recent posts first.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get the list of users the authenticated user is following
        following_users = request.user.following.all()

        # Filter posts authored by these users and order them by creation date
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at') #Post.objects.filter(author__in=following_users).order_by('-created_at')


        # Serialize the posts
        serializer = PostSerializer(posts, many=True)

        # Return the serialized posts
        return Response(serializer.data, status=status.HTTP_200_OK)    