from django.contrib.auth import get_user_model
from django.db.models.signals import pre_delete, pre_save
from django.dispatch import receiver

User = get_user_model()


@receiver(pre_save, sender=User)
def update_user_staff_status_before_save(sender, instance, **kwargs):
    # Set staff and active as parallel values
    instance.is_staff = instance.is_active
