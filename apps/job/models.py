from django.db import models
from django.contrib.auth.models import User


class Job(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Running', 'Running'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    estimated_duration = models.IntegerField(help_text="Duration in seconds")
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    deadline = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    wait_time = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.started_at and self.created_at:
            self.wait_time = self.started_at - self.created_at
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
