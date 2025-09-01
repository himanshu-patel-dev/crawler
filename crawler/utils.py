import requests
from bs4 import BeautifulSoup
import urllib.robotparser
from urllib.parse import urlparse

def is_allowed(url, user_agent="MyCrawler"):
    # parse the passed url string
    parsed = urlparse(url)
    # generate url for robots.txt
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

    rp = urllib.robotparser.RobotFileParser()
    try:
        # read the robots.txt file
        rp.set_url(robots_url)
        rp.read()
    except Exception:
        return True  # allow if robots.txt unreachable

    # check if the url can be fetched by the user agent
    return rp.can_fetch(user_agent, url)

def extract_metadata(url):
    # specify the user agent to avoid blocking
    headers = {"User-Agent": "MyCrawler/1.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    # raise requests.exceptions.HTTPError on error status codes (4xx, 5xx)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    title = soup.title.string.strip() if soup.title else ""
    description = ""
    desc_tag = soup.find("meta", attrs={"name": "description"})
    if desc_tag and desc_tag.get("content"):
        description = desc_tag["content"]

    body = " ".join([p.get_text(strip=True) for p in soup.find_all("p")])

    return {
        "title": title,
        "description": description,
        "body": body[:2000]  # truncate to avoid DB bloat
    }
