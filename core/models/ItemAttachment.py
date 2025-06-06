import uuid
from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

import core.shared.Upload_to


class ItemAttachment(models.Model):
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, db_index=True)
    object_id = models.PositiveIntegerField(db_index=True)
    attached_to = GenericForeignKey('content_type', 'object_id')

    file = models.FileField(upload_to=core.shared.Upload_to.upload_to)
    filename = models.CharField(max_length=255)
    is_original = models.BooleanField(default=False)
    version = models.PositiveIntegerField(default=1)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey('accounts.User',  on_delete=models.CASCADE)  # if needed

    class Meta:
        db_table = 'item_attachments'
        indexes = [models.Index(fields=['content_type', 'object_id'])]

    def set_version(self):
        if not self.version:
            last_version = (
                ItemAttachment.objects
                .filter(content_type=self.content_type, object_id=self.object_id, filename=self.filename)
                .aggregate(models.Max('version'))
                .get('version__max') or 0
            )
            self.version = last_version + 1


    def save(self, *args, **kwargs):
        self.set_version()
        super().save(*args, **kwargs)