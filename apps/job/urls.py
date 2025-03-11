from django.urls import path
from django.contrib.auth.decorators import login_required

from apps.job.views import DashboardView, JobListView

urlpatterns = [
    path("", login_required(DashboardView.as_view()), name="dashboard"),
    path("job/list/", login_required(JobListView.as_view()), name="job-list"),
]
