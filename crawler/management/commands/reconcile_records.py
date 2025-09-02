from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from django.db import models
from crawler.models import URLRecord

class Command(BaseCommand):
    help = "Mark stuck in-progress URLs as failed"

    def handle(self, *args, **options):
        timeout_minutes = 5 # e.g., 5 minutes
        cutoff = timezone.now() - timedelta(minutes=timeout_minutes)

        stuck_qs = URLRecord.objects.filter(
            status=URLRecord.STATUS_IN_PROGRESS,
            picked_at__lt=cutoff
        )

        count = stuck_qs.update(
            status=URLRecord.STATUS_FAILED,
            retries=models.F('retries') + 1
        )

        self.stdout.write(f"Marked {count} stuck URLs as failed.")
