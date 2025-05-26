def generate_trading_signals(analyzed_articles: list[dict]) -> list[dict]:
    """Applies the basic sentiment strategy to analyzed articles to generate trading signals."""
    trading_signals = []
    strategy_params = {'positive_threshold': 0.6}

    from app.trading_logic.sentiment_strategy import evaluate_basic_sentiment_strategy

    for article in analyzed_articles:
        signal = evaluate_basic_sentiment_strategy(article, strategy_params)
        if signal:
            trading_signals.append(signal)

    return trading_signals
