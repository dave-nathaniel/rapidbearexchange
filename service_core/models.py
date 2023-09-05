from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist



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
        return self.username



class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bvn = models.CharField(max_length=50, null=True, blank=True)
    photo = models.FileField(upload_to='verification_documents/', null=True, blank=True)
    country = models.CharField(max_length=50, default='NG')
    identity_verified = models.BooleanField(default=False)

    @property
    def ref_code(self):
        return self.username



class UserVerification(models.Model):
    verification_states = [
        ('pending', 'Pending'), 
        ('approved', 'Approved'), 
        ('rejected', 'Rejected')
    ]

    verification_methods = [
        ('passport', 'International Passport'), 
        ('license', 'Driver\'s License')
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=verification_states)
    document = models.FileField(upload_to='verification_documents/')
    submission_date = models.DateTimeField(null=True, blank=True)
    verification_date = models.DateTimeField(null=True, blank=True)
    method = models.CharField(max_length=20, choices=verification_methods)
    verification_data = models.JSONField(null=True, blank=True)
    bvn_data = models.JSONField(null=True, blank=True)
    # Add more fields as needed

    def __str__(self):
        return f"{self.user.username} - {self.status}"



class CashAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=50, unique=True)
    bank_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.account_name} - {self.account_number}"



class DigitalAsset(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, unique=True)
    market_price = models.DecimalField(
        max_digits=20, decimal_places=10
    )  # Updated market price
    # Add more fields as needed (e.g., market price, blockchain info, etc.)

    def __str__(self):
        return self.name

def create_default_assets():
    try:
        DigitalAsset.objects.get(symbol='ETH')
    except ObjectDoesNotExist:
        DigitalAsset.objects.create(name='Ethereum', symbol='ETH', market_price=0.00)

    try:
        DigitalAsset.objects.get(symbol='BTC')
    except ObjectDoesNotExist:
        DigitalAsset.objects.create(name='Bitcoin', symbol='BTC', market_price=0.00)

    try:
        DigitalAsset.objects.get(symbol='USDT')
    except ObjectDoesNotExist:
        DigitalAsset.objects.create(name='Tether', symbol='USDT', market_price=0.00)



class Wallet(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    cash_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    digital_assets = models.ManyToManyField(DigitalAsset, through="DigitalAssetBalance")

    def __str__(self):
        return f"{self.user.username}'s Wallet"



class DigitalAssetBalance(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    digital_asset = models.ForeignKey(DigitalAsset, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=10, default=0)

    def __str__(self):
        return f"{self.wallet.user.username}'s {self.digital_asset.name} Balance"



class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
        ("conversion", "Conversion"),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=10)  # Cash or digital asset symbol

    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.amount} {self.currency}"




#Signals



@receiver(post_save, sender=CustomUser)
def create_user_wallet(sender, instance, created, **kwargs):
    # TODO: Check that the user is neither a staff nor a superuser before creating a wallet for them.
    if created:
        create_default_assets()
        wallet = Wallet.objects.create(user=instance, cash_balance=0.00)

        # Create default balances for each digital asset
        for asset in DigitalAsset.objects.all():
            DigitalAssetBalance.objects.create(wallet=wallet, digital_asset=asset, balance=0.00)




post_save.connect(create_user_wallet, sender=CustomUser)