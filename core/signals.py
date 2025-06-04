from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.core.files.base import ContentFile

from core.models import Item, ItemAttachment, DecisionVotes
from accounts.models import User  # or adjust based on how to get uploader


@receiver(post_save)
def auto_attach_file(sender, instance, created, **kwargs):
    if not created:
        return

    if sender in [Item, DecisionVotes]:
        ItemAttachment.objects.create(
            content_type=ContentType.objects.get_for_model(sender),
            object_id=instance.id,
            attached_to=instance,
            file=ContentFile(b"default file contents", name="default.txt"),
            filename='default.txt',
            uploaded_by=getattr(instance, 'user', None)  # fallback if no .user
        )