from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.generic import View
from django.views import View
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from .serializers import FollowUnfollowSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'token': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(View):
    def get(self, request):
        # Handle GET request
        return render(request, 'login.html')
    

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'profile.html', {})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(CustomUser, id=user_id)
    request.user.follow(user_to_follow)
    return JsonResponse({'message': f'You are now following {user_to_follow.username}.'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
    request.user.unfollow(user_to_unfollow)
    return JsonResponse({'message': f'You have unfollowed {user_to_unfollow.username}.'})

class FollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUnfollowSerializer

    def post(self, request, *args, **kwargs):
        user_to_follow_id = kwargs.get('user_id')
        try:
            user_to_follow = CustomUser.objects.get(id=user_to_follow_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        request.user.following.add(user_to_follow)
        return Response({'message': f'You are now following {user_to_follow.username}.'}, status=status.HTTP_200_OK)


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FollowUnfollowSerializer

    def post(self, request, *args, **kwargs):
        user_to_unfollow_id = kwargs.get('user_id')
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_to_unfollow_id)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        request.user.following.remove(user_to_unfollow)
        return Response({'message': f'You have unfollowed {user_to_unfollow.username}.'}, status=status.HTTP_200_OK)
    
class ListUsersView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = FollowUnfollowSerializer    