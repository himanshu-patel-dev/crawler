# crawler/robots.py
import time
import requests
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

# cache domain -> RobotFileParser + last fetch time
robots_cache = {}
last_fetch = {}

USER_AGENT = "MyCrawlerBot/1.0 (+https://example.com/bot)"

def can_fetch(url):
    domain = urlparse(url).netloc
    if domain not in robots_cache:
        rp = RobotFileParser()
        robots_url = f"http://{domain}/robots.txt"
        try:
            resp = requests.get(robots_url, timeout=5)
            rp.parse(resp.text.splitlines())
        except Exception:
            rp = None
        robots_cache[domain] = rp
    rp = robots_cache[domain]
    if rp is None:
        return True
    return rp.can_fetch(USER_AGENT, url)

def wait_for_domain(url, min_delay=2):
    """Enforce min_delay between requests to the same domain."""
    domain = urlparse(url).netloc
    now = time.time()
    last = last_fetch.get(domain, 0)
    wait = min_delay - (now - last)
    if wait > 0:
        time.sleep(wait)
    last_fetch[domain] = time.time()
