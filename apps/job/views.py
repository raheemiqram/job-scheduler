from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.job.models import Job


class DashboardView(APIView):
    def get(self, request):
        total_jobs = Job.objects.count()
        pending_jobs = Job.objects.filter(status='Pending').count()
        running_jobs = Job.objects.filter(status='Running').count()
        completed_jobs = Job.objects.filter(status='Completed').count()

        avg_wait_time = Job.objects.filter(status='Completed').exclude(started_at=None).extra(
            select={'wait_time': "strftime('%s', started_at) - strftime('%s', created_at)"}
        ).aggregate(avg_wait_time=Avg('wait_time'))['avg_wait_time']

        return Response({
            "total_jobs": total_jobs,
            "pending_jobs": pending_jobs,
            "running_jobs": running_jobs,
            "completed_jobs": completed_jobs,
            "average_wait_time": avg_wait_time or 0
        })
