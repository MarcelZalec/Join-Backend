from django.db.models.signals import post_save
from django.dispatch import receiver
from user_auth_app.models import CustomUser

@receiver(post_save, sender=CustomUser)
def activate_admin(sender, instance, created, **kwargs):
    if created and instance.is_staff and not instance.is_active:
        instance.is_active = True
        instance.save()


@receiver(post_save, sender=CustomUser)
def activate_all_accouts_on_creation(sender, instance, created, **kargs):
    """
    This function activates the Account when it was created
    (this is for modification purposes if you maybe want to send an email for activating an account,
    until you can rewrite the code)
    """
    if created and not instance.is_active:
        instance.is_active = True
        instance.save()