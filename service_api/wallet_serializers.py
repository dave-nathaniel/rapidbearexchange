from rest_framework import serializers
from service_wallet.models import Wallet, AssetBalance
from service_markets.models import Asset, BaseAsset


class AssetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Asset
		fields = ['name', 'symbol', 'market_value', 'active', 'base_asset']


class AssetBalanceSerializer(serializers.ModelSerializer):
	asset = AssetSerializer()

	class Meta:
		model = AssetBalance
		fields = ['asset', 'balance', 'value_in_base_currency']


class WalletSerializer(serializers.ModelSerializer):
	owned_asset = AssetBalanceSerializer(many=True, read_only=True)

	class Meta:
		model = Wallet
		fields = ['user', 'based_on', 'total_balance', 'owned_asset']
