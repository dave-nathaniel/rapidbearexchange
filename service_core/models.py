from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_countries.fields import CountryField



class CustomUserManager(UserManager):
	def create_user(self, first_name, last_name, username, email, phone, date_of_birth, password=None):
		"""
		Creates and saves a User with the given email, date of
		birth and password.
		"""
		if not email:
			raise ValueError("Users must have an email address")

		user = self.model(
			first_name=first_name,
			last_name=last_name,
			username=username,
			email=self.normalize_email(email),
			phone=phone,
			date_of_birth=date_of_birth,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, first_name, last_name, username, email, phone, date_of_birth, password=None):
		"""
		Creates and saves a superuser with the given email, date of
		birth and password.
		"""
		user = self.create_user(
			first_name=first_name,
			last_name=last_name,
			username=username,
			email=email,
			phone=phone,
			date_of_birth=date_of_birth,
			password=password,
		)
		user.is_superuser = True
		user.is_staff = True
		user.save(using=self._db)
		return user



class CustomUser(AbstractUser):
	first_name = models.CharField(max_length=150)
	last_name = models.CharField(max_length=150)
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=100, unique=True)
	date_of_birth = models.DateField()
	
	objects = CustomUserManager()
	
	USERNAME_FIELD = "email"
	EMAIL_FIELD = "email"
	REQUIRED_FIELDS = ["username", "first_name", "last_name", "date_of_birth", "phone"]
	
	def __str__(self):
		return f"{self.first_name} {self.last_name}"



class UserProfile(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	photo = models.FileField(upload_to='user_images/', null=True, blank=True)
	country = CountryField()
	identity_verified = models.BooleanField(default=False)
	
	@property
	def ref_code(self):
		return self.username



class ExternalAssetAccount(models.Model):
	'''
		Accounts of external assets belonging to the user, like a Bank Account for example (fiat asset)
		or a BTC Address (digital asset).

		Presently, the sole use for this is as a "withdrawal destination".
	'''
	ASSET_TYPE_CHOICES = [
		('fiat', 'Fiat'), #FIAT asset accounts like Bank Accounts.
		('digital', 'Digital'), #Digitat asset accounts like crypto wallet.
		#('Real', 'Real') "Real" assets include assets like Gold, etc, we currently don't have need for those.
	]

	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	user_account_id = models.CharField(max_length=50) #ID of this user in that account.
	account_asset_type = models.CharField(max_length=7, choices=ASSET_TYPE_CHOICES)
	account_authority_name = models.CharField(max_length=100) #Full name of the account authority, like the bank's name for example.
	account_authority_id = models.CharField(max_length=100) #Bank codes, crypto symbols, etc.
	account_common_name = models.CharField(max_length=50) #A descriptive name (e.g. "Bank Account", "Bitcoin Wallet")
	account_meta = models.JSONField(default=dict) #Any other information we might need to store about this account.
	
	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=['account_authority_id', 'user_account_id'],
				name='authority_identifier_unique',
			),
		]
	
	def __str__(self):
		return f"{self.user.first_name} - {self.account_authority_id}"