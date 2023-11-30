from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated

from .overrides.rest_framework import APIResponse

from .user_serializers import UserRegistrationSerializer
from .user_serializers import UserSerializer
from .user_serializers import UserUpdateSerializer
from .user_serializers import CustomTokenObtainPairSerializer

from .wallet_serializers import WalletSerializer

from service_wallet.models import Wallet

from django.conf import settings


CustomUser = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
	serializer_class = CustomTokenObtainPairSerializer

	def post(self, request, *args, **kwargs):

		response = super().post(request, *args, **kwargs)

		return APIResponse('Authenticated', status.HTTP_200_OK, data=response.data)


class UserProfileAPIView(APIView):

	def post(self, request):
		serializer = UserRegistrationSerializer(data=request.data)
		try:
			if serializer.is_valid():
				user_data = serializer.validated_data
				serializer.save()
				return APIResponse('User registered successfully', status.HTTP_201_CREATED)

			return APIResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			return APIResponse(f'{e}', status.HTTP_400_BAD_REQUEST)

	def get(self, request):

		self.permission_classes = [IsAuthenticated]

		user = CustomUser.objects.get(id=request.user.id)
		user_profile = user.profile
		serializer = UserSerializer(user, context={'profile': user_profile})

		return APIResponse('User profile retreived successfully', status.HTTP_200_OK,serializer.data)

	def put(self, request):

		self.permission_classes = [IsAuthenticated]

		user = CustomUser.objects.get(id=request.user.id)
		serializer = UserUpdateSerializer(data=request.data)

		if serializer.is_valid():
			user_data = serializer.validated_data

			for attr, value in user_data.items():
				if value is not None:
					setattr(user, attr, value)

			user.save()

			return APIResponse('User information updated successfully', status.HTTP_200_OK, data=user_data)

		return APIResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)


class UserWalletAPIView(APIView):

	permission_classes = [IsAuthenticated]

	def get(self, request):
		user_wallet = Wallet.objects.get(user=request.user)
		serializer = WalletSerializer(user_wallet)

		return APIResponse('User wallet retreived successfully.', status.HTTP_200_OK, data=serializer.data)