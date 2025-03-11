from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, ExpressionWrapper, F
from django.forms import fields
from django.shortcuts import render
from django.views.generic import TemplateView, ListView

from apps.job.models import Job


class DashboardView(TemplateView):

    def get(self, request, *args, **kwargs):
        # Base query for jobs
        job_queryset = Job.objects.all() if self.request.user.is_superuser else Job.objects.filter(
            user=self.request.user)

        # Counting the total jobs, pending jobs, running jobs, and completed jobs
        total_jobs = job_queryset.count()
        pending_jobs = job_queryset.filter(status='Pending').count()
        running_jobs = job_queryset.filter(status='Running').count()
        completed_jobs = job_queryset.filter(status='Completed').exclude(started_at=None)

        # avg_wait_time = job_queryset.filter(status='Completed').exclude(started_at=None).extra(
        #     select={'wait_time': "strftime('%s', started_at) - strftime('%s', created_at)"}
        # ).aggregate(avg_wait_time=Avg('wait_time'))['avg_wait_time']


        return render(request, 'dashboard/index.html', {
            "total_jobs": total_jobs,
            "pending_jobs": pending_jobs,
            "running_jobs": running_jobs,
            "completed_jobs": completed_jobs,
            "average_wait_time": 0,
        })


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "dashboard/jobs/list.html"
    context_object_name = "jobs"
    ordering = ["-priority", "deadline"]  # Order by priority first, then by deadline

    def get_queryset(self):
        queryset = Job.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return queryset
