import re

# Simple rule-based classifier
def classify_page(title, description, content):
    """
    Determine the page type: 'product', 'blog', 'news', or 'other'
    """
    text = ' '.join([title or '', description or '', content or '']).lower()

    # Rules for product pages
    if re.search(r'\b(add to cart|price|reviews|buy now)\b', text):
        return 'product'

    # Rules for blog pages
    if re.search(r'\b(blog|how to|guide|tips)\b', text):
        return 'blog'

    # Rules for news pages
    if re.search(r'\b(news|breaking|report|journalist|CNN|BBC)\b', text):
        return 'news'

    return 'other'


def extract_topics(text):
    """
    Extract topics by finding keywords.
    For demo purposes, simple word frequency / keyword matching
    """
    text = text.lower()
    keywords = ['kitchen', 'camping', 'outdoors', 'technology', 'politics', 'news', 'blog', 'product']
    topics = [kw for kw in keywords if kw in text]
    return topics
