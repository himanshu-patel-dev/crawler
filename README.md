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
