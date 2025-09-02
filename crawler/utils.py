import hashlib
from urllib.parse import urljoin, urlparse, urldefrag

def normalize_url(base, link):
    # Resolve relative links and strip fragments
    try:
        # base = http://example.com/products/page1
        # link = ../about
        # result = http://example.com/about
        joined = urljoin(base, link)

        # Removes any fragment part (#something)
        nofrag, _ = urldefrag(joined)

        # break URL into parts
        # {
        #   scheme: 'http',
        #   netloc: 'Example.COM:80',
        #   path: '/page',
        #   query: 'id=5'
        # }
        parsed = urlparse(nofrag)
        # Normalize: lowercase scheme and host
        scheme = parsed.scheme.lower()  # https or http
        netloc = parsed.netloc.lower()  # example.com
        path = parsed.path or '/'
        normalized = f"{scheme}://{netloc}{path}"

        # append the query params if present
        if parsed.query:
            normalized += f"?{parsed.query}"
        return normalized
    except Exception:
        return None

# return a sha256 hash of the text
def content_hash(text: str) -> str:
    h = hashlib.sha256()
    h.update(text.encode('utf-8', errors='ignore'))
    return h.hexdigest()
