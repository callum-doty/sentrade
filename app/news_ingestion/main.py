from app.news_ingestion.scrapers.rss_scraper import fetch_articles_from_rss, parse_rss_article

def run_news_ingestion_pipeline(sources_config: list[dict]) -> list[dict]:
    """Orchestrates the fetching and initial processing of news from RSS sources."""
    articles = []
    for source in sources_config:
        if source['type'] == 'rss':
            rss_url = source['url']
            raw_articles = fetch_articles_from_rss(rss_url)
            for raw_article in raw_articles:
                article = parse_rss_article(raw_article)
                articles.append(article)
    return articles

def store_raw_articles(articles: list[dict]):
    """Stores raw fetched articles into the database/data store."""
    {}
