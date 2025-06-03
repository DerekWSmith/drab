from django.db import models

'''
Through tables for accept and block list
Really, just a placeholder at the moment
'''
class UserAcceptlist(models.Model):
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.DO_NOTHING,
        related_name='accepted_users',
        db_index=True
    )
    accepted_user = models.ForeignKey(
        'accounts.User',
        on_delete=models.DO_NOTHING,
        related_name='accepted_by_users',
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'useracceptlist'
        # unique_together = ('user', 'accepted_user')