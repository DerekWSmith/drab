from django.db import models

class UserBlocklist(models.Model):
    user = models.ForeignKey(
        'accounts.User',

        on_delete=models.DO_NOTHING,
        related_name='blocked_users',
        db_index=True,
        db_constraint=False
    )
    blocked_user = models.ForeignKey(
        'accounts.User',

        on_delete=models.DO_NOTHING,
        related_name='blocked_by_users',
        db_index=True,
        db_constraint=False
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'userblocklist'
        # unique_together = ('blocker', 'blocked')


