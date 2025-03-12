from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
import random
from datetime import timedelta

from apps.job.models import Job


class Command(BaseCommand):
    help = 'Create sample jobs with random data'

    def handle(self, *args, **kwargs):
        admin, created = User.objects.get_or_create(username='admin', email='admin@example.com')
        admin.set_password("admin")
        admin.is_superuser = True
        admin.save()

        # Create a sample user
        user, created = User.objects.get_or_create(username='sample_user', email='sample_user@example.com')
        user.set_password("1234")
        user.save()

        # Define sample job priorities and statuses
        priorities = [1, 2, 3]
        statuses = ['Pending', 'Completed', 'Failed']

        # Generate sample jobs
        for i in range(10):  # Change the range to generate more/less sample data
            priority = random.choice(priorities)
            status = random.choice(statuses)
            deadline = timezone.now() + timedelta(days=random.randint(1, 30))  # Random deadline within 30 days
            estimated_duration = random.randint(60, 120)  # Random estimated duration between 1 min to 1 hour

            job = Job.objects.create(
                user=user,
                name=f"Sample Job {i + 1}",
                estimated_duration=estimated_duration,
                priority=priority,
                deadline=deadline,
                status=status,
                created_at=timezone.now(),
                started_at=timezone.now() + timedelta(minutes=random.randint(1, 20)),
                completed_at=timezone.now() + timedelta(minutes=random.randint(1, 30))
            )

            self.stdout.write(self.style.SUCCESS(f"Successfully created job: {job.name}"))
