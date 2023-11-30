from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CustomUser, UserProfile
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
	# TODO: Check that the user is neither a staff nor a superuser before creating a wallet for them.
	if created and not (instance.is_staff or instance.is_superuser):
		UserProfile.objects.create(user=instance)



