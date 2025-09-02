import time
import json
import redis
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from crawler.models import URLRecord, Page
from crawler.extractor import extract_basic
from crawler.classifier import classify_page, extract_topics
from crawler.utils import normalize_url, content_hash
from crawler.robots import can_fetch, wait_for_domain

REDIS_KEY = getattr(settings, 'CRAWLER_REDIS_QUEUE_KEY', 'crawler:queue')
REDIS_URL = getattr(settings, 'CRAWLER_REDIS_URL', 'redis://localhost:6379/0')
USER_AGENT = 'MyCrawlerBot/1.0 (+https://example.com/bot)'


class Command(BaseCommand):
    help = 'Fetcher worker: consumes urls from redis queue and processes them'

    def add_arguments(self, parser):
        parser.add_argument('--sleep', type=float, default=1.0)

    def handle(self, *args, **options):
        sleep = options['sleep']
        r = redis.from_url(REDIS_URL)
        self.stdout.write('Fetcher worker started...')

        while True:
            # fetch task from redis queue
            task = self.get_task(r)
            if not task:
                # to decrease polling rate
                # and save cpu cycles when
                # queue is empty
                time.sleep(sleep)
                continue

            # fetch URLRecord from DB 
            urlrec = self.get_url_record(task['url_id'])
            if not urlrec:
                continue

            # check for robots.txt
            if not can_fetch(task['url']):
                self.stderr.write(f"Blocked by robots.txt: {task['url']}")
                self.update_url_status(urlrec, 'blocked')
                continue
            # respect crawl delay
            wait_for_domain(task['url'])

            # fetch content of the URL
            self.stdout.write(f"Fetching {task['url']} (id={urlrec.id})")
            try:
                html = self.fetch_url(task['url'])
                title, description, main_text, links = extract_basic(html, task['url'])
                page = self.save_page(urlrec, title, description, main_text)
                self.update_url_status(urlrec, 'done')
                self.enqueue_links(links)
                self.stdout.write(f"Processed {task['url']} → {page.page_type}")
            except Exception as e:
                self.update_url_status(urlrec, 'failed', increment_fail=True)
                self.stderr.write(f"Failed {task['url']}: {e}")

    def get_task(self, redis_conn):
        packed = redis_conn.blpop(REDIS_KEY, timeout=5)
        if not packed:
            return None
        _, raw = packed
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            self.stderr.write(f'Bad payload: {e}')
            return None

    def get_url_record(self, url_id):
        urlrec = URLRecord.objects.filter(id=url_id).first()
        if not urlrec:
            self.stderr.write(f'No URLRecord {url_id}')
        return urlrec

    def fetch_url(self, url):
        headers = {'User-Agent': USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        return resp.text

    def save_page(self, urlrec, title, description, main_text):
        c_hash = content_hash((title or '') + (description or '') + (main_text or ''))
        dup = Page.objects.filter(content_hash=c_hash).first()

        if dup:
            page, _ = Page.objects.update_or_create(
                url=urlrec,
                defaults={
                    'title': title,
                    'description': description,
                    'content': main_text,
                    'content_hash': c_hash,
                    'page_type': dup.page_type,
                    'topics': dup.topics,
                }
            )
        else:
            ptype = classify_page(title, description, main_text)
            topics = extract_topics(' '.join([title or '', description or '', main_text or '']))
            page, _ = Page.objects.update_or_create(
                url=urlrec,
                defaults={
                    'title': title,
                    'description': description,
                    'content': main_text,
                    'content_hash': c_hash,
                    'page_type': ptype,
                    'topics': topics,
                }
            )
        return page

    def update_url_status(self, urlrec, status, increment_fail=False):
        urlrec.status = status
        if increment_fail:
            urlrec.retries += 1
        urlrec.save(update_fields=['status', 'retries'] if increment_fail else ['status'])

    def enqueue_links(self, links):
        # Optional: push new links to Redis or DB
        for link in links:
            normalized = normalize_url(link, link)
            if normalized:
                URLRecord.objects.get_or_create(url=normalized, defaults={'status': 'pending'})
