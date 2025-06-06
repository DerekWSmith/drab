import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from accounts.models.User import User


class ItemSubscription(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User,  on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    last_read = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)