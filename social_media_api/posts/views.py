from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, status, generics
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType

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

class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if not post:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        if Like.objects.filter(user=request.user, post=post).exists():
            return Response({"error": "You already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Create Like
        Like.objects.create(user=request.user, post=post)

        # Create Notification
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post,
        )

        return Response({"message": "Post liked successfully."}, status=status.HTTP_200_OK)


class UnlikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = Post.objects.filter(pk=pk).first()
        if not post:
            return Response({"error": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

        like = Like.objects.filter(user=request.user, post=post).first()
        if not like:
            return Response({"error": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete Like
        like.delete()

        return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)    

class LikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Retrieve the post or return a 404 if it doesn't exist
        post = generics.get_object_or_404(Post, pk=pk)

        # Create a like or get an existing one
        like, created = Like.objects.get_or_create(user=request.user, post=post)

        if not created:
            return Response({"message": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        # Generate a notification for the post's author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target=post
            )

        return Response({"message": "Post liked successfully."}, status=status.HTTP_201_CREATED)

class UnlikePostView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        # Retrieve the post or return a 404 if it doesn't exist
        post = generics.get_object_or_404(Post, pk=pk)

        # Try to find the like
        like = Like.objects.filter(user=request.user, post=post).first()

        if not like:
            return Response({"message": "You haven't liked this post yet."}, status=status.HTTP_400_BAD_REQUEST)

        # Delete the like
        like.delete()

        return Response({"message": "Post unliked successfully."}, status=status.HTTP_200_OK)    