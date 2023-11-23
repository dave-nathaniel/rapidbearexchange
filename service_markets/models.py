from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class AbstractAsset(models.Model):
	ASSET_TYPE_CHOICES = [
		('fiat', 'Fiat'), #FIAT asset accounts like Bank Accounts.
		('digital', 'Digital'), #Digitat asset accounts like crypto wallet.
		#('Real', 'Real') "Real" assets include assets like Gold, etc, we currently don't have need for those.
	]

	name = models.CharField(max_length=100)
	symbol = models.CharField(max_length=10, unique=True)
	asset_type = models.CharField(max_length=7, default='digital', choices=ASSET_TYPE_CHOICES)
	active = models.BooleanField(default=False)
	market_value = models.DecimalField(max_digits=30, decimal_places=10, default=1.0)
	metadata = models.JSONField(default=dict, blank=True)

	def __str__(self):
		return f"{self.name} ({self.symbol})"

	class Meta:
		abstract = True


class BaseAsset(AbstractAsset):
	'''
		Base assets exist to be a reference for the value of an asset. The market value of a 
		base asset is ALWAYS 1.0.
		For example, given USD as a base asset, if the market value of NGN is 200, that
		means 1 USD = 200 NGN.
	'''
	def save(self, *args, **kwargs):

		super().save(*args, **kwargs)

		# Check if this is the first instance in the database
		if BaseAsset.objects.count() == 1:
			for item in Asset.objects.filter(base_asset__isnull=True):
				item.base_asset = self
				item.save()


class Asset(AbstractAsset):
	base_asset = models.ForeignKey(BaseAsset, null=True, on_delete=models.SET_NULL)

	@property
	def market_value(self, ):
		#Override the parent property
		try:
			return self.market.latest().value
		except ObjectDoesNotExist:
			return 0.00

	def __str__(self):
		return f"{self.symbol} | (1 {self.symbol} is currently {round(float(self.market_value), 5)} {self.base_asset.symbol})"


class Market(models.Model):
	GAIN_DIRECTION = "up"
	LOSS_DIRECTION = "down"

	CHANGE_DIRECTION_CHOICES = [
		(GAIN_DIRECTION, "Rising"),
		(LOSS_DIRECTION, "Falling"),
	]

	asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='market')
	value = models.DecimalField(max_digits=30, decimal_places=10)
	timestamp = models.DateTimeField(auto_now_add=True)
	change_direction = models.CharField(max_length=4, editable=False, default=GAIN_DIRECTION, choices=CHANGE_DIRECTION_CHOICES)

	def save(self, *args, **kwargs):
		# Get the last inserted market instance for this asset
		last_market = Market.objects.filter(asset=self.asset).order_by('-timestamp').first()
		# try:
		# 	if self.value == last_market.value:
			
		# except Exception as e:
		# 	raise e

		if last_market:
			# Calculate the profit/loss
			if self.value > last_market.value:
				self.change_direction = self.GAIN_DIRECTION
			else:
				self.change_direction = self.LOSS_DIRECTION
		else:
			# If this is the first market entry, consider it as profit
			self.change_direction = self.GAIN_DIRECTION

		super().save(*args, **kwargs)


	class Meta:
		get_latest_by = "timestamp"
		default_permissions = ('add', 'view')