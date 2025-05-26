def evaluate_basic_sentiment_strategy(article_with_sentiment: dict, strategy_params: dict) -> dict | None:
    """
    Evaluates a single article based on sentiment to generate a trading signal.
    Returns a signal (e.g., {'action': 'BUY', 'symbol': 'XYZ', 'confidence': 0.8}) or None.
    """
    sentiment_score = article_with_sentiment.get('sentiment_score')
    symbol = article_with_sentiment.get('ticker')

    if not sentiment_score or not symbol:
        return None

    positive_threshold = strategy_params.get('positive_threshold', 0.5)
    
    if sentiment_score > positive_threshold:
        return {
            'action': 'BUY',
            'symbol': symbol,
            'confidence': 0.8
        }

    return None
