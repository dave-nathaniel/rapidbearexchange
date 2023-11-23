from django.db import models
from django.contrib.auth import get_user_model
from service_core.models import ExternalAssetAccount
from service_wallet.models import Wallet
from service_markets.models import Asset


CustomUser = get_user_model()

INCOMING_TX = "inbound"
OUTGOING_TX = "outbound"

TRANSACTION_STATUS = (
	(-1, "Failed"),
	(0, "Pending"),
	(1, "Successful"),
)



class PaymentGateway(models.Model):
	name = models.CharField(max_length=100, null=False, blank=False)
	service_icon = models.URLField(max_length=150, null=True, blank=True)
	service_url = models.URLField(max_length=200)
	transaction_types = models.JSONField(
		max_length=20, 
		default=list,
	)
	added_on = models.DateField(auto_now_add=True)
	metadata = models.JSONField(default=dict)



class Transaction(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	asset = models.ForeignKey(Asset, on_delete=models.CASCADE)  # Cash or digital asset symbol
	value = models.DecimalField(max_digits=15, decimal_places=2)
	status = models.SmallIntegerField(default=0, choices=TRANSACTION_STATUS)
	verified = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)
	metadata = models.JSONField(default=dict)

	class Meta:
		abstract = True


class OutgoingTransaction(Transaction):
	transaction_type = models.CharField(
		max_length=20,
		default=OUTGOING_TX
	)
	source = models.ForeignKey(Wallet, on_delete=models.CASCADE)
	destination = models.ForeignKey(
		ExternalAssetAccount,
		default="External Account",
		on_delete=models.SET_DEFAULT,
	)


class IncomingTransaction(Transaction):
	transaction_type = models.CharField(
		max_length=20,
		default=INCOMING_TX
	)
	source = models.ForeignKey(
		PaymentGateway, 
		on_delete=models.CASCADE,
	)
	destination = models.ForeignKey(Wallet, on_delete=models.CASCADE)