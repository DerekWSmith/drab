import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class Group(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=200)
    creator = models.ForeignKey(

        settings.AUTH_USER_MODEL,

        on_delete=models.CASCADE,
        related_name='created_groups',
        db_constraint=False
    )
    is_auto = models.BooleanField(default=False)  # True for same-domain groups
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_groups'
        unique_together = ('name', 'creator')  # Optional: prevent duplicates per creator

    def __str__(self):
        return self.name
