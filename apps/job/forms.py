from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["name", "estimated_duration", "priority", "deadline"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter job name"}),
            "estimated_duration": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Duration in seconds"}),
            "priority": forms.Select(attrs={"class": "form-control"}),
            "deadline": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }
