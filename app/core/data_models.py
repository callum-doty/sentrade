from pydantic import BaseModel
from typing import Optional, List

class Article(BaseModel):
    id: Optional[str] = None
    source: str
    url: str
    title: str
    content: str
    publish_date: Optional[str] = None # Consider datetime object
    scraped_at: Optional[str] = None # Consider datetime object
    sentiment_score: Optional[float] = None
    sentiment_label: Optional[str] = None # e.g., 'positive', 'negative', 'neutral'
    stock_mentions: Optional[List[str]] = []

class TradingSignal(BaseModel):
    symbol: str
    action: str # 'BUY', 'SELL', 'HOLD'
    source_article_id: Optional[str] = None
    strategy_name: str
    confidence: Optional[float] = None
    timestamp: str # Consider datetime object
    # Potentially add price targets, stop-loss levels

class ExecutedTrade(BaseModel):
    signal_id: Optional[str] = None
    broker_order_id: str
    symbol: str
    action: str
    quantity: float
    fill_price: float
    status: str # 'FILLED', 'PARTIALLY_FILLED', 'REJECTED'
    timestamp: str # Consider datetime object