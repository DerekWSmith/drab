from django.db import models
from core.models.Item import Item
from django.utils import timezone
from django.conf import settings
import math

from accounts.models.User import User

class ActiveActivityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
class CompletedActivityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_completed=True)

class UnCompletedActivityManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_completed=False)

class Activity(Item):

    objects = models.Manager()
    active = ActiveActivityManager()
    completed = CompletedActivityManager()
    uncompleted = UnCompletedActivityManager()

    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    pre_requisites = models.ManyToManyField('self', symmetrical=False, related_name='unlock_tasks', blank=True) # tasks must be finished, before this one can start
    requisites = models.ManyToManyField('self', symmetrical=False, related_name='complete_with_tasks', blank=True) # tasks must be finished, before this can finish
    team = models.ManyToManyField(User, symmetrical=False, related_name='allocated_team', blank=True) # Users allocated to this task

    effort_minutes = models.PositiveIntegerField(default=0, help_text="Estimated total effort in minutes")
    slack_minutes = models.PositiveIntegerField(default=0, help_text="Buffer time in minutes")
    duration_minutes = models.PositiveIntegerField(default=60, help_text="Base duration excluding slack")

    is_active = models.BooleanField(default=True)

    status = models.CharField(max_length=50, default='pending', help_text="Status of the task (e.g., pending, in_progress, blocked, completed)")
    priority = models.PositiveIntegerField(default=3, help_text="Priority from 1 (high) to 5 (low)")

    blocked_by = models.ManyToManyField('self', symmetrical=False, related_name='blocks', blank=True)

    start_date = models.DateField(null=True, blank=True, help_text="Scheduled or actual start date")
    completed_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when task was completed")

    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='owned_tasks', help_text="Primary owner of the task")
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_tasks', help_text="Person reviewing this task")

    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags for this task")
    category = models.CharField(max_length=100, blank=True, help_text="Optional task category")

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities_created', help_text="User who created the task")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities_updated', help_text="User who last updated the task")
    change_log = models.TextField(blank=True, help_text="Optional log of task changes")

    estimated_start = models.DateField(null=True, blank=True, help_text="Estimated start date")
    estimated_end = models.DateField(null=True, blank=True, help_text="Estimated end date")
    actual_start = models.DateField(null=True, blank=True, help_text="Actual start date")
    actual_end = models.DateField(null=True, blank=True, help_text="Actual end date")


    @property
    def total_estimated_minutes(self):
        return self.duration_minutes + self.slack_minutes

    @property
    def total_estimated_hours(self):
        return self.total_estimated_minutes / 60

    @property
    def total_estimated_days(self):
        days = self.total_estimated_minutes / (60 * settings.WORK_DAY_HOURS)
        return math.ceil(days * 100) / 100  # rounds up to 2 decimal places (days.hours)

    @property
    def total_estimated_weeks(self):
        weeks = self.total_estimated_days / settings.WORK_WEEK_DAYS
        return math.ceil(weeks * 100) / 100  # rounds up to 2 decimal places (weeks.days)

    @property
    def days_elapsed(self):
        return (timezone.now().date() - self.created_at.date()).days

    @property
    def days_to_deadline(self):
        if self.due_date:
            return (self.due_date - timezone.now().date()).days
        return None

    class Meta:
        db_table = 'ItemActivities'
