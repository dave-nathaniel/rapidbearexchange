from rest_framework import serializers
from service_core.models import UserProfile
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django_countries.serializers import CountryFieldMixin


CustomUser = get_user_model()


class UserProfileSerializer(CountryFieldMixin, serializers.ModelSerializer):
	ref_code = serializers.SerializerMethodField()
	verification = serializers.SerializerMethodField()

	def get_ref_code(self, obj):
		return obj.ref_code

	def get_verification(self, obj):
		return obj.profile_verification

	class Meta:
		model = UserProfile
		exclude = ["id", "user"]
		# fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
	profile = UserProfileSerializer()
	class Meta:
		model = CustomUser
		fields = [
			'id', 
			'first_name', 
			'last_name', 
			'username', 
			'email', 
			'phone', 
			'date_of_birth', 
			'last_login', 
			'date_joined',
			'profile',
		]
		

class UserRegistrationSerializer(serializers.Serializer):
	email = serializers.EmailField()
	username = serializers.CharField(max_length=100)
	password = serializers.CharField(write_only=True)
	firstname = serializers.CharField(max_length=100)
	lastname = serializers.CharField(max_length=100)
	phone = serializers.CharField(max_length=100)
	date_of_birth = serializers.DateField()

	def create(self, validated_data):
		password = make_password(validated_data.get('password'))
		instance = CustomUser.objects.create(
			email=validated_data['email'],
			username=validated_data['username'],
			password=password,
			first_name=validated_data['firstname'],
			last_name=validated_data['lastname'],
			phone=validated_data['phone'],
			date_of_birth=validated_data['date_of_birth'],
		)
		
		return instance


class UserUpdateSerializer(serializers.Serializer):
	firstname = serializers.CharField(max_length=100, required=False)
	lastname = serializers.CharField(max_length=100, required=False)
	phone = serializers.CharField(max_length=100, required=False)
	date_of_birth = serializers.DateField(required=False)
	country = serializers.CharField(max_length=50, required=False)
	# Add more fields as needed for user information update


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
	@classmethod
	def get_token(cls, user):
		token = super().get_token(user)
		# Add custom claims to the token, if needed
		return token

	def validate(self, attrs):
		data = super().validate(attrs)
		user = self.user or self.context['request'].user
		# Include user information in the response
		data['user'] = {
			'id': user.id,
			'username': user.username,
			'email': user.email,
			'firstname': user.first_name,
			'lastname': user.last_name,
			'phone': user.phone,
			'date_of_birth': user.date_of_birth,
		}

		return data