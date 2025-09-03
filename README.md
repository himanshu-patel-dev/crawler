# web crawler
a simple web crawler

## How to insert URLs from Django shell

```bash
python3 manage.py shell
```
```python
from crawler.models import URLRecord

URLRecord.objects.create(url="http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/")
URLRecord.objects.create(url="http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/")
URLRecord.objects.create(url="http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/")
```

## Manually run workers to queue URLs or clean dead/stuck URLs

```bash
# pick urls in 'queued' or 'failed' with <5 reties and push them to queue
$ python manage.py dispatch_urls --batch 5
Pushed 1 urls to queue

# when fetch worker fails - URL remain 'in progress' in DB
# reconcile worker those to 'failed' and increase retry count by 1
$ $ python manage.py reconcile_records
Marked 0 stuck URLs as failed

# celery worker to consume task
celery -A crawler_service worker -l info -Q crawler
# flower - celery UI
celery -A crawler_service flower --port=5555

```

## Links

#### API Endpoints
- `http://127.0.0.1:8000/api/urls/` - post new URL and this will be picked up by dispatcher

![URL POST API](images/url_post_api.png)

- `http://127.0.0.1:8000/api/urls/list/` - show all URLs along with their status

![URL GET API](images/url_get_api.png)

- `http://localhost:5555/` - dashboard for celery task workers

![Celery Dashboard](images/celery_dashboard.png)

- `http://127.0.0.1:8000/admin/` - admin dashboard

![Admin Dashboard](images/admin_dashboard.png)

- `http://127.0.0.1:8000/admin/crawler/page/5/change/` - admin page to view crawled page
![alt text](images/crawled_page.png)

## ToDo
- Check query access patterns and Indexes

