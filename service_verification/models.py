from django.db import models
from django.contrib.auth import get_user_model


CustomUser = get_user_model()


VERIFICATION_STATES = [
	(0, 'Initiated'),
	(1, 'Approved'), 
	(-1, 'Rejected'),
]

def get_sentinel_user():
	#The first created super user becomes the default control staff of any verification process.
	return CustomUser.objects.filter(is_superuser=True).order_by('id').first()


class Verification(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	status = models.SmallIntegerField(
		default=0, 
		choices=VERIFICATION_STATES
	)
	metadata = models.JSONField(default=dict)
	submitted_on = models.DateTimeField(auto_now_add=True)
	last_updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class ID_Verification(Verification):
	
	ID_VERIFICATION_METHODS = [
		('passport', 'International Passport'), 
		('license', 'Driver\'s License')
	]
	
	method = models.CharField(max_length=20, choices=ID_VERIFICATION_METHODS)
	id_document = models.FileField(upload_to='verification_documents/', null=True)
	reviewed_by = models.ForeignKey(CustomUser, related_name="reviewed_by", on_delete=models.SET(get_sentinel_user))
	review_notes = models.TextField()
	
	def __str__(self):
		return f"{self.user.username} - {self.status}"


class BVN_Verification(Verification):
	bvn = models.CharField(max_length=15, null=False, unique=True)
	bvn_access_authorization = models.JSONField(default=dict)