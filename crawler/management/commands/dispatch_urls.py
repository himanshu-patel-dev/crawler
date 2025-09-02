from django.core.management.base import BaseCommand
from crawler.models import URLRecord
from crawler.tasks import fetch_url_task
import redis
import json
from django.conf import settings
from django.utils import timezone
from django.db.models import Q


# Configure REDIS_URL in Django settings
REDIS_KEY = getattr(settings, 'CRAWLER_REDIS_QUEUE_KEY', 'crawler:queue')
REDIS_URL = getattr(settings, 'CRAWLER_REDIS_URL', 'redis://localhost:6379/0')


class Command(BaseCommand):
    help = 'Dispatcher: push pending URLs into Redis queue in batches'

    def add_arguments(self, parser):
        parser.add_argument('--batch', type=int, default=50)


    def handle(self, *args, **options):
        batch = options['batch']
        r = redis.from_url(REDIS_URL)

        # Select up to `batch` urls
        qs = URLRecord.objects.filter(
            Q(status=URLRecord.STATUS_PENDING) |
            Q(status=URLRecord.STATUS_FAILED, retries__lt=5)
        ).order_by("id")  # deterministic batch

        url_batch = list(qs[:batch])

        # Mark them in-progress
        URLRecord.objects.filter(id__in=[u.id for u in url_batch]).update(
            status=URLRecord.STATUS_IN_PROGRESS,
            picked_at=timezone.now()
        )

        for urlrec in url_batch:
            fetch_url_task.apply_async(
                args=[urlrec.id, urlrec.url],
                queue="crawler"
            )
            self.stdout.write(f"Dispatched {urlrec.url} (id={urlrec.id})")
