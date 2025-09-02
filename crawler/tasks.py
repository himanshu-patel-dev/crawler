# crawler/tasks.py
from celery import shared_task
import requests
from crawler.models import URLRecord, Page
from crawler.extractor import extract_basic
from crawler.classifier import classify_page, extract_topics
from crawler.utils import content_hash

USER_AGENT = "MyCrawlerBot/1.0 (+https://example.com/bot)"

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def fetch_url_task(self, url_id, url):
    """Fetch the URL, extract content, classify and store in DB."""
    urlrec = URLRecord.objects.get(id=url_id)
    headers = {"User-Agent": USER_AGENT}
    resp = requests.get(url, headers=headers, timeout=15)
    resp.raise_for_status()

    title, desc, text, links = extract_basic(resp.text, url)
    c_hash = content_hash((title or '') + (desc or '') + (text or ''))

    Page.objects.update_or_create(
        url=urlrec,
        defaults={
            "title": title,
            "description": desc,
            "content": text,
            "content_hash": c_hash,
            "page_type": classify_page(title, desc, text),
            "topics": extract_topics(' '.join([title or '', desc or '', text or ''])),
        },
    )
    urlrec.status = URLRecord.STATUS_DONE
    urlrec.save()
    return url
