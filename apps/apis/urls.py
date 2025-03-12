from django.urls import path
from .views import JobListCreateView, JobStatusAPIView

urlpatterns = [
    path('jobs/', JobListCreateView.as_view(), name='job-list-api'),
    path('jobs/<int:pk>/', JobStatusAPIView.as_view(), name='job-status-api'),
]
