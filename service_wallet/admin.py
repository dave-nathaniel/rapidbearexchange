from django.contrib import admin
from .models import Wallet, AssetBalance

class AssetBalanceAdmin(admin.ModelAdmin):
	list_display = ('asset', 'wallet')
	
	def get_readonly_fields(self, request, obj=None):
		# If obj is None, it's a new object being created, so allow editing.
		if obj is None:
			return []
		# If obj exists, it's an existing object, so make all fields readonly.
		return [field.name for field in obj._meta.fields]


class WalletAdmin(admin.ModelAdmin):
	list_display = ('user', 'get_assets', 'total_balance')

	@admin.display(description='owned assets')
	def get_assets(self, obj):
		return ", ".join([a.asset.symbol for a in obj.owned_asset.all()])

	def get_readonly_fields(self, request, obj=None):
		# If obj is None, it's a new object being created, so allow editing.
		if obj is None:
			return []
		# If obj exists, it's an existing object, so make all fields readonly.
		return [field.name for field in obj._meta.fields]

admin.site.register(Wallet, WalletAdmin)
admin.site.register(AssetBalance, AssetBalanceAdmin)
