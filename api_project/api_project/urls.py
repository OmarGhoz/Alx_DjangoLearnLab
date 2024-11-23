from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),  # Include api app's URLs
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import BookList, BookViewSet
from .views import BookViewSet

# Initialize the router
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

# Define URL patterns
urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # Existing endpoint for listing books
    path('', include(router.urls)),  # Include all routes from the router
]

from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/', include('api.urls')),  # Assuming your app's API urls are under 'api.urls'
]
