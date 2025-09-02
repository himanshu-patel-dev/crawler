from rest_framework import serializers
from .models import URLRecord

class URLRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = URLRecord
        fields = ["id", "url", "status", "retries", "picked_at"]
        read_only_fields = ["id", "status", "retries", "picked_at"]
