from django.db import models
from django.conf import settings
from django.utils import timezone
from accounts.models.Group import Group


class GroupMembership(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='group_memberships'
    )
    group = models.ForeignKey(
        to=Group,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    start_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_read = models.DateTimeField(null=True, blank=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, default='')

    class Meta:
        db_table = 'group_memberships'
        unique_together = ('user', 'group')