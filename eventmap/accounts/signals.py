from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from allauth.account.signals import user_signed_up

from .models import Profiles


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(
            user=instance,
            name=instance.username,
        )

@receiver(post_save, sender=user_signed_up)
def create_social_profile(sender, instance, user_logged_in, **kwargs):
    if user_logged_in:
        Profiles.objects.create(
            user=instance,
            name=instance.username,
        )
