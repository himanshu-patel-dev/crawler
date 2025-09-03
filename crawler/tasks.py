# crawler/tasks.py
from celery import shared_task
import requests
from crawler.models import URLRecord, Page
from crawler.extractor import extract_basic
from crawler.classifier import classify_page, extract_topics
from crawler.utils import content_hash
from urllib.parse import urlparse
from crawler.robots import wait_for_domain

# USER_AGENT = "MyCrawlerBot/1.0 (+https://example.com/bot)"
MAX_RETRIES = 3  # max retries stored in DB or use a fixed number

@shared_task(bind=True, autoretry_for=(requests.RequestException,), retry_backoff=True, max_retries=MAX_RETRIES)
def fetch_url_task(self, url_id, url):
    """Fetch the URL, extract content, classify and store in DB."""
    urlrec = URLRecord.objects.get(id=url_id)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
                    (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.amazon.com/"
    }

    # headers = {"User-Agent": USER_AGENT}

    try:
        domain = urlparse(url).netloc
        wait_for_domain(domain)  # respect crawl delay

        # fetch the URL
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()

        # extract content
        title, desc, text, links = extract_basic(resp.text, url)
        # generate hash of content
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

    except requests.RequestException as e:
        print(f"HTTP error while fetching {url}: {e}")
        # Increment retry count
        urlrec.retries += 1
        if urlrec.retries >= MAX_RETRIES:
            urlrec.status = URLRecord.STATUS_FAILED
            urlrec.last_error = f"Reached max retries ({MAX_RETRIES})"
            urlrec.save()
        else:
            urlrec.save()
            raise self.retry(exc=e)
    except Exception as e:
        print(f"Unhandled error while fetching {url}: {e}")
        # Parsing or DB errors → fail immediately
        urlrec.retries += 1
        urlrec.status = URLRecord.STATUS_FAILED
        urlrec.last_error = f"Processing failed: {str(e)}"
        urlrec.save()
