from bs4 import BeautifulSoup
from typing import Tuple, List


def extract_basic(html: str, url: str) -> Tuple[str, str, str, List[str]]:
    """
        Returns: title, description, main_text, extracted_links
    """
    soup = BeautifulSoup(html, 'lxml')

    # Title heuristics
    title = ''
    h1 = None
    if soup.title and soup.title.string:
        title = soup.title.string.strip()
        h1 = soup.find('h1')
    if h1 and h1.get_text(strip=True):
        # prefer h1 if title not present
        title = h1.get_text(strip=True)

    # Meta description
    description = ''
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    if desc_tag and desc_tag.get('content'):
        description = desc_tag['content'].strip()

    # Simple main text extraction: join <p> text
    paragraphs = [p.get_text(separator=' ', strip=True) for p in soup.find_all('p')]
    main_text = '\n'.join([p for p in paragraphs if p])

    # Extract links
    links = []
    for a in soup.find_all('a', href=True):
        links.append(a['href'])

    return title, description, main_text, links
