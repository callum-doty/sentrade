# app/run_pipeline_test.py
import sys
import os

# Add the project root directory (sentrade) to sys.path
# This allows the script to be run directly as `python app/run_pipeline_test.py`
# and still find the 'app' module.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

"""
Test script to run a simplified version of the new multi-strategy pipeline.
This script demonstrates the integration of the Portfolio Manager (EWAAllocator)
and individual strategies (SentimentStrategy, MeanReversionStrategy).
"""

from app.portfolio_manager.ewa_allocator import EWAAllocator
from app.strategies.sentiment_strategy.main import SentimentStrategy
from app.strategies.mean_reversion_strategy.main import MeanReversionStrategy
from app.data_ingestion.news_main import run_news_ingestion_pipeline
from app.trading_logic.main import DEFAULT_NEWS_SOURCES_CONFIG

# from app.feature_engineering import some_feature_processor # Placeholder


def run_test():
    print("--- Initializing Test Pipeline ---")

    # 1. Initialize Portfolio Manager (EWAAllocator)
    strategy_names = ["SentimentStrategy", "MeanReversionStrategy"]
    ewa_allocator = EWAAllocator(strategies=strategy_names, learning_rate=0.1)
    print(f"Initialized EWA Allocator for strategies: {strategy_names}")
    print(f"Initial Allocations: {ewa_allocator.get_allocations()}")

    # 2. Initialize Strategies
    # Configurations can be empty or have mock/test values
    sentiment_strategy_config = {"mock_param_sentiment": "value1"}
    sentiment_strategy = SentimentStrategy(strategy_config=sentiment_strategy_config)
    print(f"Initialized {sentiment_strategy.get_name()}")

    mean_reversion_strategy_config = {
        "lookback_period": 10,
        "std_dev_threshold": 1.5,
    }  # Test values
    mean_reversion_strategy = MeanReversionStrategy(
        strategy_config=mean_reversion_strategy_config
    )
    print(f"Initialized {mean_reversion_strategy.get_name()}")

    print("\n--- Simulating Trading Period 1 ---")

    # 3. Data Ingestion for Sentiment Strategy (using Yahoo RSS Feed)
    print("\nFetching real news articles for Sentiment Strategy...")
    raw_articles_from_rss = run_news_ingestion_pipeline(
        sources_config=DEFAULT_NEWS_SOURCES_CONFIG
    )

    processed_sentiment_articles = []
    if raw_articles_from_rss:
        print(f"Fetched {len(raw_articles_from_rss)} articles from RSS feed.")
        for article in raw_articles_from_rss:
            # Mocking ticker extraction for the test
            tickers = []
            content_lower = (
                article.get("title", "") + article.get("content", "")
            ).lower()
            if "aapl" in content_lower or "apple" in content_lower:
                tickers.append("AAPL")
            if "goog" in content_lower or "google" in content_lower:
                tickers.append("GOOG")
            if "msft" in content_lower or "microsoft" in content_lower:
                tickers.append("MSFT")

            processed_sentiment_articles.append(
                {
                    "id": article.get(
                        "link", article.get("title", "rss_article")
                    ),  # Use link or title as ID
                    "content": article.get("content", ""),
                    "tickers_mentioned": list(set(tickers)),  # Ensure unique tickers
                }
            )
    else:
        print(
            "No articles fetched from RSS. Sentiment strategy might not produce signals."
        )

    sentiment_input_data = {"articles": processed_sentiment_articles}

    if processed_sentiment_articles:
        print("\nSample of articles processed for Sentiment Strategy (first 3):")
        for i, article_data in enumerate(processed_sentiment_articles[:3]):
            print(f"  Article {i+1}:")
            print(f"    ID/Link: {article_data.get('id', 'N/A')}")
            print(
                f"    Content Snippet: {article_data.get('content', '')[:100]}..."
            )  # Print first 100 chars
            print(f"    Mocked Tickers: {article_data.get('tickers_mentioned', [])}")
    else:
        print("\nNo articles were processed for Sentiment Strategy to show samples.")

    # For MeanReversionStrategy (still using mock data)
    mock_mean_reversion_data = {
        "XCORP": {  # Assuming XCORP is a stock symbol
            "prices": [100, 102, 101, 103, 102, 98, 97, 99, 100, 95],  # Lookback 10
            "current_price": 95,
        },
        "YINC": {
            "prices": [50, 51, 52, 53, 54, 55, 58, 57, 56, 60],
            "current_price": 60,
        },
    }
    print("Mock data prepared.")

    # 4. Generate Signals from each strategy
    sentiment_signals = sentiment_strategy.generate_signals(sentiment_input_data)
    print(f"\nSignals from {sentiment_strategy.get_name()}:")
    for signal in sentiment_signals:
        print(f"  {signal}")

    mean_reversion_signals = mean_reversion_strategy.generate_signals(
        mock_mean_reversion_data
    )
    print(f"\nSignals from {mean_reversion_strategy.get_name()}:")
    for signal in mean_reversion_signals:
        print(f"  {signal}")

    # 5. (Optional) Simulate Consolidated Trade Decision based on EWA Allocations
    # This would involve taking signals and current EWA weights to form a portfolio trade.
    # For this test, we'll focus on the EWA update.
    current_allocations = ewa_allocator.get_allocations()
    print(f"\nCurrent EWA Allocations before performance update: {current_allocations}")

    # 6. Simulate Performance Feedback for EWA Allocator
    # Performance can be P&L, Sharpe, or any agreed-upon metric.
    # Using the strategy's own get_performance for this test.
    sentiment_perf = sentiment_strategy.get_performance()
    mean_reversion_perf = mean_reversion_strategy.get_performance()

    # EWAAllocator expects performance values (higher is better).
    # The current get_performance() in placeholders returns dicts like {'pnl': ..., 'trades_executed': ...}
    # We need to extract a single performance metric, e.g., P&L for simplicity.
    strategy_performance_feedback = {
        "SentimentStrategy": sentiment_perf.get("pnl", 0),
        "MeanReversionStrategy": mean_reversion_perf.get("pnl", 0),
    }
    print(f"\nSimulated Performance Feedback:")
    print(f"  Sentiment P&L: {strategy_performance_feedback['SentimentStrategy']}")
    print(
        f"  Mean Reversion P&L: {strategy_performance_feedback['MeanReversionStrategy']}"
    )

    ewa_allocator.update_weights(strategy_performance_feedback)
    print(
        f"\nUpdated EWA Allocations after Period 1 performance: {ewa_allocator.get_allocations()}"
    )

    print("\n--- Simulating Trading Period 2 (example with different performance) ---")
    # Reset mock P&L in strategies for a new period if they accumulate internally
    # (Current placeholders do this, which is fine for this test)
    sentiment_strategy.historical_performance = {"pnl": 0.0, "trades_executed": 0}
    mean_reversion_strategy.historical_performance = {"pnl": 0.0, "trades_executed": 0}

    # For Period 2, we can re-use the fetched articles or fetch new ones.
    # For simplicity in this test, we'll re-use or use a smaller mock set if fetching failed.
    # Or, to show EWA changes, let's make sentiment perform differently.
    # We'll use a simpler mock for P2 sentiment to control its P&L easily.
    mock_sentiment_data_p2 = {
        "articles": [
            {
                "id": "test_news_p2_1",
                "content": "AAPL had a neutral day.",  # Should not trigger strong signals in placeholder
                "tickers_mentioned": ["AAPL"],
            }
        ]
    }
    mock_mean_reversion_data_p2 = {
        "XCORP": {
            "prices": [95, 96, 94, 93, 95, 97, 98, 99, 100, 102],
            "current_price": 102,  # Moved up
        }
    }
    sentiment_signals_p2 = sentiment_strategy.generate_signals(
        mock_sentiment_data_p2
    )  # Should be no signal or sell
    mean_reversion_signals_p2 = mean_reversion_strategy.generate_signals(
        mock_mean_reversion_data_p2
    )  # Should be sell

    sentiment_perf_p2 = sentiment_strategy.get_performance()
    mean_reversion_perf_p2 = mean_reversion_strategy.get_performance()
    strategy_performance_feedback_p2 = {
        "SentimentStrategy": sentiment_perf_p2.get(
            "pnl", 0
        ),  # Assume sentiment did poorly
        "MeanReversionStrategy": mean_reversion_perf_p2.get(
            "pnl", 0
        ),  # Assume MR did well
    }
    print(f"\nSimulated Performance Feedback (Period 2):")
    print(f"  Sentiment P&L: {strategy_performance_feedback_p2['SentimentStrategy']}")
    print(
        f"  Mean Reversion P&L: {strategy_performance_feedback_p2['MeanReversionStrategy']}"
    )

    ewa_allocator.update_weights(strategy_performance_feedback_p2)
    print(
        f"\nUpdated EWA Allocations after Period 2 performance: {ewa_allocator.get_allocations()}"
    )

    print("\n--- Test Pipeline Run Finished ---")


if __name__ == "__main__":
    run_test()
