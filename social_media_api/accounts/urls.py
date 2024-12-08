from django.urls import path
from .views import RegisterView
from .views import LoginView
from . import views
from .views import ProfileView


urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),  # Route for registration
    path('login/', views.LoginView.as_view(), name='login'),  # Route for login
    path('profile/', views.ProfileView.as_view(), name='profile'),  # Route for user profile
]
