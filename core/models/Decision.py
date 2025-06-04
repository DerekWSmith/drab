from django.db import models

from accounts.models.User import User
from core.models.Item import Item
from core.models.Activity import Activity






class Decision(Item):

    @property
    def recommended_outcome(self):
        yays, nays, all_voters = set(), set(), set()
        for v in self.votes.all():
            all_voters.add(v.voter.id)
            if v.is_yay is True:
                yays.add(v.voter.id)
            elif v.is_yay is False:
                nays.add(v.voter.id)

        # 1. Mandatory voters must all have voted
        if self.mandatory_voters.exists():
            mandatory = set(self.mandatory_voters.values_list('id', flat=True))
            if not mandatory.issubset(all_voters):
                return 'undecided'

        # 2. Veto group unanimous yay
        if self.veto_group.exists():
            veto = set(self.veto_group.values_list('id', flat=True))
            if veto.issubset(yays):
                return 'Veto group decision: yay'
            if veto.issubset(nays):
                return 'Veto group decision: nay'
            return 'Veto group decision: undecided'

        # 3. Fallback to quorum
        if len(all_voters) < self.quorum:
            return 'Quorum not reached: undecided'
        return 'Quorum decision: yay' if len(yays) > len(nays) else 'Quorum decision: nay'

    # Fields
    resolution = models.CharField(max_length=255, blank=True)
    adopted_date = models.DateTimeField(auto_now_add=True, blank=True)



    quorum = models.PositiveIntegerField(default=0, blank=True)  # total votes required if no special groups apply.
    majority = models.PositiveIntegerField(default=0, blank=True)  # passing threshold.
    veto_group = models.ManyToManyField(User, related_name='veto_decisions', blank=True)  # all must vote identically to adopt
    mandatory_voters = models.ManyToManyField(User, related_name='mandatory_vote_decisions', blank=True)  # all must vote (vote value doesn’t have to match).  Other people can vote, but these must be included.
    tags = models.CharField(max_length=250, db_index=True, default='', blank=True)

    class Meta:
        db_table = 'ItemDecisions'
