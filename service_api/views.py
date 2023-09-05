from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .overrides.rest_framework import APIResponse

from django.conf import settings


CustomUser = get_user_model()

class UserRegistrationAPIView(APIView):

	def post(self, request):
		serializer = UserRegistrationSerializer(data=request.data)

		if serializer.is_valid():
			user_data = serializer.validated_data

			serializer.save()

			return APIResponse('User registered successfully', status.HTTP_201_CREATED)

		return APIResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)



class CustomTokenObtainPairView(TokenObtainPairView):
	# Customize the response format if needed
	
	serializer_class = CustomTokenObtainPairSerializer

	def post(self, request, *args, **kwargs):

		response = super().post(request, *args, **kwargs)

		return APIResponse('Authenticated', status.HTTP_200_OK, data=response.data)



class UserUpdateAPIView(APIView):

	permission_classes = [IsAuthenticated]  # Add IsAuthenticated authentication

	def put(self, request, pk):
		user = CustomUser.objects.get(pk=pk)
		serializer = UserUpdateSerializer(data=request.data)

		if serializer.is_valid():
			user_data = serializer.validated_data

			for attr, value in user_data.items():
				if value is not None:
					setattr(user, attr, value)

			user.save()

			return APIResponse('User information updated successfully', status.HTTP_200_OK, data=user_data)

		return APIResponse(serializer.errors, status.HTTP_400_BAD_REQUEST)
