from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import JobSerializer
from ..job.models import Job
from ..job.schedulers import run_scheduler


class JobListCreateView(generics.ListCreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Job.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        run_scheduler()
