from django.urls import path
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def dashboard_view(request):
    return render(request, "dashboard/index.html")  # Dashboard template

urlpatterns = [
    path("", login_required(dashboard_view), name="dashboard"),
]
