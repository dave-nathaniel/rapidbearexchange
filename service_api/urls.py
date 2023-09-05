from django.urls import path, include
from .views import UserRegistrationAPIView, CustomTokenObtainPairView, UserUpdateAPIView


urlpatterns = [
    # Add other URL patterns
    path('register', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('authenticate', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/<int:pk>/update', UserUpdateAPIView.as_view(), name='user-update'),
]
