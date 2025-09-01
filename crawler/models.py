from django.db import models


class Page(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.url
