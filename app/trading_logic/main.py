from app.data_ingestion.news_main import run_news_ingestion_pipeline
from app.sentiment_analysis.main import (
    process_articles_for_sentiment,
    analyze_sentiment_and_generate_signals,
)

# Define a default configuration for news sources for simplicity
DEFAULT_NEWS_SOURCES_CONFIG = [
    {
        "type": "rss",
        "url": "https://feeds.finance.yahoo.com/rss/2.0/headline?s=AAPL,GOOG,MSFT&region=US&lang=en-US",  # Example RSS feed
        "name": "Yahoo Finance Tech Headlines",
    }
]


def run_trading_logic_pipeline(news_sources_config: list[dict] = None) -> list[dict]:
    """
    Orchestrates the full pipeline:
    1. Ingests news articles.
    2. Processes articles for sentiment.
    3. Analyzes sentiment to generate trading signals.
    """
    if news_sources_config is None:
        news_sources_config = DEFAULT_NEWS_SOURCES_CONFIG

    # 1. Ingest news articles
    # Assuming run_news_ingestion_pipeline returns articles with 'content' key
    raw_articles = run_news_ingestion_pipeline(sources_config=news_sources_config)
    if not raw_articles:
        print("No articles ingested. Skipping further processing.")
        return []

    # 2. Process articles for sentiment
    # process_articles_for_sentiment expects list of dicts with 'content'
    # and returns list of dicts like {'ticker': 'AAPL', 'sentiment_score': 0.7, ...}
    analyzed_articles_with_sentiment = process_articles_for_sentiment(raw_articles)
    if not analyzed_articles_with_sentiment:
        print("No articles processed for sentiment. Skipping signal generation.")
        return []

    # 3. Analyze sentiment to generate trading signals
    # analyze_sentiment_and_generate_signals expects data like the output of process_articles_for_sentiment
    trading_signals = analyze_sentiment_and_generate_signals(
        analyzed_articles_with_sentiment
    )

    return trading_signals


def log_trading_signals(signals: list[dict]):
    """Logs the generated trading signals."""
    if signals:
        for signal in signals:
            # Ensure keys exist before accessing to prevent KeyErrors
            action = signal.get("action", "N/A")
            symbol = signal.get("symbol", "N/A")
            confidence = signal.get("confidence", "N/A")
            print(
                f"Trading Signal: Action: {action}, Symbol: {symbol}, Confidence: {confidence}"
            )
    else:
        print("No trading signals generated.")


# Example of how to run the pipeline (optional, can be in a main script)
if __name__ == "__main__":
    print("Running trading logic pipeline...")
    # To make this runnable, we need to ensure dummy implementations for:
    # - app.data_ingestion.scrapers.rss_scraper.fetch_articles_from_rss
    # - app.data_ingestion.scrapers.rss_scraper.parse_rss_article
    # - app.sentiment_analysis.analyzer.get_sentiment_score
    # - app.sentiment_analysis.analyzer.identify_stock_mentions
    # - app.sentiment_analysis.decision_engine.generate_trading_signals
    # For now, this script will attempt to run with existing (potentially placeholder) functions.

    # For a simple test, we need to ensure the imported functions can run.
    # Let's assume the underlying scrapers and analyzers have basic placeholders if not fully implemented.

    # Mocking underlying functions for a simple test run if they are not implemented
    # This is complex to do here without modifying other files.
    # The goal is to connect the structure. Actual running requires all parts.

    signals = run_trading_logic_pipeline()
    log_trading_signals(signals)
    print("Trading logic pipeline finished.")
