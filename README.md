# crawler
a simple web crawler

how to use
- Start server, `python3 manage.py runserver`
- Post URL and crawler will crawl the page and store it in DB and return in API response


## API Contract

### Insert a new URL to crawl
POST `http://127.0.0.1:8000/api/crawl`
```curl
$ curl -X POST http://127.0.0.1:8000/api/crawl/ \
     -H "Content-Type: application/json" \
     -d '{"url":"https://www.cnn.com/2013/06/10/politics/edward-snowden-profile/"}'

{"url":"https://www.cnn.com/2013/06/10/politics/edward-snowden-profile/","title":"Man behind NSA leaks says he did it to safeguard privacy, liberty | CNN Politics","description":"Edward Snowden might never live in the U.S. as a free man again after leaking secrets about a U.S. surveillance program","body":"Unclear where Snowden will wind up, after leaving Hong Kong for Russia Edward Snowden, 29, is the source of leaks over an NSA surveillance program \"The public needs to decide whether these programs ... are right or wrong,\" he says He’s a high school dropout who worked his way into the most secretive...","created_at":"2025-09-01T15:02:49.384606Z","updated_at":"2025-09-01T15:02:49.384638Z"}
```

```python
from crawler.models import URLRecord

URLRecord.objects.create(url="http://www.amazon.com/Cuisinart-CPT-122-Compact-2-Slice-Toaster/dp/B009GQ034C/")
URLRecord.objects.create(url="http://blog.rei.com/camp/how-to-introduce-your-indoorsy-friend-to-the-outdoors/")
URLRecord.objects.create(url="http://www.cnn.com/2013/06/10/politics/edward-snowden-profile/")
```

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


## ToDo
- Check query access patterns and Indexes

