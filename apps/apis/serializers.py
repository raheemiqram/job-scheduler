from rest_framework import serializers

from apps.job.models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = ['status', 'started_at', 'completed_at', 'user']


class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['status']
