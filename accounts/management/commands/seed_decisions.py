# core/management/commands/seed_decisions.py
from datetime import timedelta
import random
from uuid import uuid4

from faker import Faker

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils import timezone

from core.models import Decision
from accounts.models.User import User


class Command(BaseCommand):
    help = 'Seed the database with sample decisions'

    def handle(self, *args, **kwargs):

        fake = Faker()

        users = list(User.objects.all())
        if not users:
            raise Exception("No users found")

        def get_random_user():
            return random.choice(users)

        for _ in range(10):
            d = Decision(
                uid=uuid4(),
                publish_from=timezone.now(),
                publish_until=timezone.now() + timedelta(days=random.randint(5, 30)),
                is_active=random.choice([True, False]),
                summary=fake.sentence(),
                notes=fake.text(),
                resolution=random.choice([True, False]),
                adopted_date=timezone.now() - timedelta(days=random.randint(0, 100)),
                quorum=random.randint(1, 10),
                majority=random.randint(1, 10),
                creator=get_random_user(),
                responsible=get_random_user(),
                next_responsible=get_random_user(),
                previous_id=None  # or set an existing Decision id if needed
            )
            d.save()

        self.stdout.write(self.style.SUCCESS('Successfully seeded decisions'))