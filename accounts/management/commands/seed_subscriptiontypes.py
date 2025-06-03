# yourapp/management/commands/seed_subscriptiontypes.py

from django.core.management.base import BaseCommand
from accounts.models import SubscriptionType

class Command(BaseCommand):
    help = 'Seed SubscriptionType table with initial data'

    def handle(self, *args, **kwargs):
        if SubscriptionType.objects.exists():
            self.stdout.write('SubscriptionTypes already seeded.')
            return

        types = ['Free', 'Basic', 'Premium']
        SubscriptionType.objects.bulk_create([SubscriptionType(code=t, label=t) for t in types])
        self.stdout.write('SubscriptionTypes seeded successfully.')