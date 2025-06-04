from django.db import models
from django.utils import timezone


from accounts.models.User import User




class ActiveItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class InactiveItemManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=False)

class Item(models.Model):

    @property
    def related_activities(self):
        return self.activities.all()

    @property
    def active_activities(self):
        return self.activities.filter(is_active=True)



    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_created_items')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_responsible_items', null=True,
                                    blank=True)
    next_responsible = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='%(class)s_next_responsible_items', null=True, blank=True)

    admins = models.ManyToManyField(User, related_name='%(class)s_administers_items', blank=True)
    subscribers = models.ManyToManyField(User, related_name='%(class)s_subscribed_items')

    publish_from = models.DateTimeField(default=timezone.now)
    publish_until = models.DateTimeField(null=True, blank=True)

    previous = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='%(class)s_superseded_by')

    activities = models.ManyToManyField('core.Activity', related_name='%(class)s_related_items', blank=True) # activities related to the concrete Brief, Task, Decision.

    is_active = models.BooleanField(default=True)

    objects = models.Manager()  # All
    active = ActiveItemManager()  # Only active
    inactive = InactiveItemManager()  # Only inactive



    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    referenced_at = models.DateTimeField(auto_now=True)  # can be overridden by the view, to state when last read



    def save(self, *args, **kwargs):
        if not self.responsible:
            self.responsible = self.creator
        super().save(*args, **kwargs)

    # forward in time (newer decisions)
    def get_superseding_chain(self):
        chain = []
        current = self
        while current.superseded_by.exists():
            current = current.superseded_by.first()
            chain.append(current)
        return chain

    # backward in time (older decisions)
    def get_history_chain(self):
        chain = []
        current = self
        while current.previous:
            current = current.previous
            chain.append(current)
        chain.reverse()
        return chain



    class Meta:
        abstract = True
        ordering = ('-created_at',)

