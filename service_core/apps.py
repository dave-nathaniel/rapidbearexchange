from django.apps import AppConfig


class ServiceCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'service_core'

    def ready(self):
        from django.db.models.signals import post_save
        from .models import CustomUser
        from . import signals

        post_save.connect(signals.create_user_profile, sender=CustomUser)