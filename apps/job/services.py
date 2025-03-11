from django.db.models import Avg

from apps.job.utils import format_duration


def get_dashboard_analytics(job_queryset):
    total_jobs = job_queryset.count()
    pending_jobs = job_queryset.filter(status='Pending').count()
    running_jobs = job_queryset.filter(status='Running').count()
    completed_jobs = job_queryset.filter(status='Completed').count()
    failed_jobs = job_queryset.filter(status='Failed').count()

    high_jobs = job_queryset.filter(priority='High').count()
    medium_jobs = job_queryset.filter(priority='Medium').count()
    low_jobs = job_queryset.filter(priority='Low').count()

    avg_wait_time = job_queryset.filter(status='Completed').aggregate(avg_wait=Avg('wait_time'))
    data = {
        "total_jobs": total_jobs,
        "pending_jobs": pending_jobs,
        "running_jobs": running_jobs,
        "completed_jobs": completed_jobs,
        "failed_jobs": failed_jobs,
        "high_jobs": high_jobs,
        "medium_jobs": medium_jobs,
        "low_jobs": low_jobs,
        "average_wait_time": format_duration(avg_wait_time['avg_wait']) if avg_wait_time['avg_wait'] else None
    }
    return data
