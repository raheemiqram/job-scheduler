from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, CreateView

from apps.job.forms import JobForm
from apps.job.models import Job
from apps.job.schedulers import run_scheduler
from apps.job.services import get_dashboard_analytics


class DashboardView(TemplateView):

    def get(self, request, *args, **kwargs):
        job_queryset = Job.objects.all() if self.request.user.is_superuser else Job.objects.filter(
            user=self.request.user)
        data = get_dashboard_analytics(job_queryset)
        if self.request.user.is_superuser:
            return render(request, 'dashboard/index.html', data)
        else:
            return redirect(reverse_lazy('job-list'))


class JobListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = "dashboard/jobs/list.html"
    context_object_name = "jobs"
    ordering = ["-priority", "deadline"]

    def get_queryset(self):
        queryset = Job.objects.all()
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        context['pending_jobs'] = queryset.filter(status='Pending')
        context['running_jobs'] = queryset.filter(status='Running')
        context['completed_jobs'] = queryset.filter(status='Completed')

        return context


class JobCreateView(LoginRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "dashboard/jobs/form.html"
    success_url = reverse_lazy("job-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Jobs create successfully")
        run_scheduler()
        return response
