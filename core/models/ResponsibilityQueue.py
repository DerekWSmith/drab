import uuid
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from accounts.models.User import User

class ResponsibilityQueue(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')


    assigned_to = models.ForeignKey(User,  on_delete=models.CASCADE,
        db_constraint=False)
    completed = models.BooleanField(default=False)
    notes = models.TextField()
    timestamp_completed = models.DateTimeField(auto_now=True)


    order = models.PositiveIntegerField()


    class Meta:
        ordering = ['order']