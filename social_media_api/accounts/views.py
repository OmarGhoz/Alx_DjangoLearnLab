from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer
from .serializers import PostSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import View
from django.views import View
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import FollowUnfollowSerializer
from rest_framework.authtoken.models import Token


# Get the custom user model
CustomUser = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    Handles user registration.
    """
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        # Create authentication token for the new user
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"message": "User registered successfully", "token": token.key}, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    Handles user login and returns authentication token.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # Create or retrieve token
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Allows users to view and update their profile.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class FollowUserView(generics.GenericAPIView):
    """
    Allows a user to follow another user.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Fetch target user to follow
        target_user = CustomUser.objects.filter(id=user_id).first()
        if not target_user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.add(target_user)
        return Response({"message": f"You are now following {target_user.username}"}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    """
    Allows a user to unfollow another user.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        # Fetch target user to unfollow
        target_user = CustomUser.objects.filter(id=user_id).first()
        if not target_user:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if target_user == request.user:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        request.user.following.remove(target_user)
        return Response({"message": f"You have unfollowed {target_user.username}"}, status=status.HTTP_200_OK)


class FollowingListView(generics.ListAPIView):
    """
    Displays the list of users the authenticated user is following.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.following.all()

    def list(self, request, *args, **kwargs):
        following = self.get_queryset()
        data = [{"id": user.id, "username": user.username} for user in following]
        return Response(data, status=status.HTTP_200_OK)


class FollowersListView(generics.ListAPIView):
    """
    Displays the list of users following the authenticated user.
    """
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
     
    def get_queryset(self):
        return self.request.user.followers.all()

    def list(self, request, *args, **kwargs):
        followers = self.get_queryset()
        data = [{"id": user.id, "username": user.username} for user in followers]
        return Response(data, status=status.HTTP_200_OK)
    

class PostListView(generics.ListAPIView):
    """
    View to list posts from users the authenticated user is following.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        # Get the users that the current user is following
        following_users = self.request.user.following.all()
        # Fetch posts authored by these users, ordered by creation date
        return Post.objects.filter(author__in=following_users).order_by('-created_at')


class PostCreateView(generics.CreateAPIView):
    """
    View to create a new post.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        # Save the post with the authenticated user as the author
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific post.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def get_queryset(self):
        # Ensure users can only access their own posts or posts by authors they follow
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users) | Post.objects.filter(author=self.request.user)    
    
