import uuid
from django.db import models
from django.conf import settings
from core.models.Activity import Activity

from core.models.Decision import Decision

class DecisionVote(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    decision = models.ForeignKey(Decision,

                                 on_delete=models.CASCADE,
                                 related_name='votes',
        db_constraint=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,  db_index=True,  on_delete=models.CASCADE)
    is_yay = models.BooleanField()
    voted_at = models.DateTimeField(auto_now_add=True)

    # Not yet sure whether DecisionVotes =can get an activity list
    # activities = models.ManyToManyField(Activity, related_name='activities', blank=True)  # activities related this DevisionVote.


    comments = models.TextField()

    class Meta:
        unique_together = ('decision', 'user')
        db_table = 'decision_votes'

