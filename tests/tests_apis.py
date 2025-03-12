from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta
from rest_framework.reverse import reverse_lazy
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from apps.job.models import Job


class JobAPITestCase(TestCase):

    def setUp(self):
        """Set up test users and initial data."""
        self.user = User.objects.create_user(username="user", password="password")
        self.admin = User.objects.create_superuser(username="admin", password="adminpassword")

        self.job1 = Job.objects.create(
            user=self.user,
            name="User Job",
            estimated_duration=1,
            priority=1,
            deadline=now() + timedelta(hours=1),
            status="Completed"
        )

        self.job2 = Job.objects.create(
            user=self.admin,
            name="Admin Job",
            estimated_duration=1,
            priority=2,
            deadline=now() + timedelta(hours=2),
            status="Completed"
        )
        self.client = APIClient()
        self.job_list_url = reverse_lazy('job-list-api')
        self.token_url = "/api/v1/token/"  # Adjust this if you have a different JWT login endpoint.

    def get_jwt_token(self, user):
        """Helper method to generate JWT token for a user."""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def authenticate(self, user):
        """Helper method to authenticate using JWT."""
        token = self.get_jwt_token(user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_job(self):
        """Test job creation API for authenticated users."""
        self.authenticate(self.user)

        data = {
            "name": "New Test Job",
            "estimated_duration": 1,
            "priority": 3,
            "deadline": (now() + timedelta(days=1)).isoformat(),
        }

        response = self.client.post(self.job_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Test Job")
        self.assertEqual(response.data["status"], "Pending")

    def test_job_list_user(self):
        """Test that a normal user can only see their own jobs."""
        self.authenticate(self.user)
        response = self.client.get(self.job_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "User Job")

    def test_job_list_admin(self):
        """Test that an admin can see all jobs."""
        self.authenticate(self.admin)
        response = self.client.get(self.job_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_job_status(self):
        """Test fetching job status for an authorized user."""
        self.authenticate(self.user)

        response = self.client.get(reverse_lazy('job-status-api', kwargs={'pk': self.job1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Completed")

    def test_job_status_unauthorized(self):
        """Test that a user cannot fetch another user's job status."""
        self.authenticate(self.user)

        response = self.client.get(reverse_lazy('job-status-api', kwargs={'pk': self.job2.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_job_status_admin(self):
        """Test that an admin can fetch any job status."""
        self.authenticate(self.admin)

        response = self.client.get(reverse_lazy('job-status-api', kwargs={'pk': self.job1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Completed")

    def test_unauthenticated_access(self):
        """Test that unauthenticated users cannot access job list."""
        response = self.client.get(self.job_list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
