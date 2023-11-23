from django.urls import path, include
from .views import UserRegistrationAPIView, CustomTokenObtainPairView, UserUpdateAPIView


urlpatterns = [
    # Add other URL patterns
    path('user/register', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('user/authenticate', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/<int:pk>/update', UserUpdateAPIView.as_view(), name='user-update'),
]
