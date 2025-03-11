from rest_framework import generics
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from .serializers import JobSerializer, JobStatusSerializer
from ..job.models import Job
from ..job.schedulers import run_scheduler


class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Job.objects.all()
        return Job.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # better to handle via celery (async)
        run_scheduler()


class JobStatusAPIView(RetrieveAPIView):
    serializer_class = JobStatusSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Job.objects.all()
        return Job.objects.filter(user=self.request.user)
