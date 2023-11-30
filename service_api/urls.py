from django.urls import path, include
from .views import CustomTokenObtainPairView, UserProfileAPIView
from .views import UserWalletAPIView


urlpatterns = [
    # Add other URL patterns
    path('user/register', UserProfileAPIView.as_view(), name='user-registration'),
    path('user/authenticate', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/profile', UserProfileAPIView.as_view(), name='user-profile'),
    path('user/update', UserProfileAPIView.as_view(), name='user-update'),

    path('user/wallet', UserWalletAPIView.as_view(), name='user-update'),
]
