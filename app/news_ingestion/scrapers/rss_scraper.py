import feedparser
import time # For potential future use like adding delays

def fetch_articles_from_rss(rss_url: str) -> list[dict]:
    """
    Fetches articles from a given RSS feed URL using feedparser.
    Returns a list of feedparser entry objects (which are dict-like).
    """
    try:
        print(f"Fetching articles from RSS feed: {rss_url}")
        feed = feedparser.parse(rss_url)
        if feed.bozo: # Check for malformed feed
            print(f"Warning: Feed {rss_url} may be malformed. Bozo reason: {feed.bozo_exception}")
        # feed.entries is a list of dictionaries, one for each article
        print(f"Fetched {len(feed.entries)} entries from {rss_url}")
        return feed.entries # These are already dict-like
    except Exception as e:
        print(f"Error fetching RSS feed {rss_url}: {e}")
        return []

def parse_rss_article(article_entry: dict) -> dict:
    """
    Parses a single raw article entry from feedparser into a structured format.
    The sentiment analysis part expects a 'content' key.
    """
    # Extracting common fields. feedparser entries are dictionaries.
    title = article_entry.get('title', 'No Title')
    link = article_entry.get('link', '')
    published_date = article_entry.get('published', article_entry.get('updated', ''))
    
    # Try to get content: 'summary', 'description', or join 'content' array if present
    content = article_entry.get('summary', article_entry.get('description', ''))
    if not content and 'content' in article_entry and isinstance(article_entry['content'], list):
        # Sometimes content is a list of content objects
        content_parts = [c.get('value', '') for c in article_entry['content'] if c.get('value')]
        content = "\n".join(content_parts)

    # Ensure content is a string
    if not isinstance(content, str):
        content = str(content) if content is not None else ''

    parsed_article = {
        'title': title,
        'link': link,
        'published_date': published_date,
        'content': content, # Key expected by sentiment analysis
        'source_type': 'rss',
        'original_entry': article_entry # Keep original for more detailed parsing if needed later
    }
    # print(f"Parsed article: {title[:50]}...") # For debugging
    return parsed_article
