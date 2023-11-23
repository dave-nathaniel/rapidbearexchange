from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from service_markets.models import Asset, BaseAsset
from django.contrib import admin


CustomUser = get_user_model()


class Wallet(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, unique=True)
	based_on = models.ForeignKey(BaseAsset, null=True, on_delete=models.SET_NULL)

	@property
	@admin.display(description='total balance')
	def total_balance(self):
		return sum(item.value_in_base_currency() for item in self.owned_asset.all())

	def __str__(self):
		return f"{self.user.first_name}'s Wallet ({self.user.email})"


class AssetBalance(models.Model):
	wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='owned_asset')
	asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
	balance = models.DecimalField(max_digits=29, decimal_places=20, default=0)

	def value_in_base_currency(self, ):
		'''
			This is how much the balance of this particular asset is worth in the
			base currency. 
			E.g. the asset balance is $1, the base currency is Naira, and the exchange rate is $1 = 100 naira, then the "value_in_base_currency" will be 500 (naira). Because that's how much you "actually" have.
		'''
		return float(self.asset.market_value) * float(self.balance)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=['wallet', 'asset'],
				name='wallet_asset_unique',
			),
		]
	
	def __str__(self):
		return f"Balance = {float(self.balance)} | Value = {float(self.asset.market_value) * float(self.balance)} {self.asset.base_asset.symbol}"