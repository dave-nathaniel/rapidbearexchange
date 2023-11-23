from django.dispatch import receiver
from django.db.models.signals import post_save
from service_core.models import CustomUser
from service_markets.models import Asset, BaseAsset
from service_wallet.models import Wallet, AssetBalance
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=CustomUser)
def create_user_wallet(sender, instance, created, **kwargs):

	base_asset = BaseAsset.objects.all().order_by("id").first()
	
	def create_default_assets():

		try:
			Asset.objects.get(symbol='NGN')
		except ObjectDoesNotExist:
			Asset.objects.create(name='Naira', symbol='NGN', base_asset=base_asset, active=True)

		try:
			Asset.objects.get(symbol='BTC')
		except ObjectDoesNotExist:
			Asset.objects.create(name='Bitcoin', symbol='BTC', base_asset=base_asset, active=False)

		try:
			Asset.objects.get(symbol='ETH')
		except ObjectDoesNotExist:
			Asset.objects.create(name='Ethereum', symbol='ETH', base_asset=base_asset, active=False)

		try:
			Asset.objects.get(symbol='USDT')
		except ObjectDoesNotExist:
			Asset.objects.create(name='Tether', symbol='USDT', base_asset=base_asset, active=False)

	
	# TODO: Check that the user is neither a staff nor a superuser before creating a wallet for them.
	if created and not (instance.is_staff or instance.is_superuser):
		wallet = Wallet.objects.create(user=instance, based_on=base_asset)
		create_default_assets()

		# Create default balances for each digital asset
		for asset in Asset.objects.filter(active=True):
			AssetBalance.objects.create(wallet=wallet, asset=asset, balance=0.00)



