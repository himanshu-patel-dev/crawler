from django.db import models
from django.utils import timezone

class URLRecord(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_IN_PROGRESS, 'In progress'),
        (STATUS_DONE, 'Done'),
        (STATUS_FAILED, 'Failed'),
    ]

    url = models.URLField(unique=True, max_length=2000)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_PENDING)
    retries = models.IntegerField(default=0)
    last_error = models.TextField(blank=True, null=True)
    last_fetched = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    picked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'url_table'

    def __str__(self):
        return f"{self.url} ({self.status})"


class Page(models.Model):
    url = models.OneToOneField(URLRecord, on_delete=models.CASCADE, related_name='page')
    title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    content_hash = models.CharField(max_length=128, db_index=True)
    page_type = models.CharField(max_length=64, blank=True, null=True)
    topics = models.JSONField(blank=True, null=True) # list of strings
    fetched_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'page'

    def __str__(self):
        return f"Page for {self.url.url}"
