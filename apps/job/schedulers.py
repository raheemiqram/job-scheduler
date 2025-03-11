import threading
import time
from django.utils.timezone import now
from .models import Job
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .services import get_dashboard_analytics

MAX_CONCURRENT_JOBS = 3
running_jobs = 0


def process_job(job):
    global running_jobs
    job.status = 'Running'
    job.started_at = now()
    job.save()

    try:
        time.sleep(job.estimated_duration)  # Simulate job execution
        job.status = 'Completed'
        job.completed_at = now()
        job.save()
    except Exception:  # assuming failure in job execution  task
        job.status = 'Failed'
        job.completed_at = now()
        job.save()

    running_jobs -= 1

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "dashboard_analytics",
        {
            "type": "send_dashboard_data",
            "message": get_dashboard_analytics(Job.objects.all())
        }
    )

    run_scheduler()


def run_scheduler():
    global running_jobs
    if running_jobs >= MAX_CONCURRENT_JOBS:
        return

    pending_jobs = Job.objects.filter(status='Pending').order_by('-priority', 'deadline')
    for job in pending_jobs:
        if running_jobs < MAX_CONCURRENT_JOBS:
            running_jobs += 1
            threading.Thread(target=process_job, args=(job,)).start()
