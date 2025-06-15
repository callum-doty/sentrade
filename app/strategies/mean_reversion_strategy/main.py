# app/strategies/mean_reversion_strategy/main.py
from app.strategies.base_strategy import BaseStrategy

# Placeholder for actual data models or specific data handling
# from app.core.data_models import TradingSignal


class MeanReversionStrategy(BaseStrategy):
    """
    Trading strategy based on the principle of mean reversion,
    betting that prices will revert to their historical mean.
    """

    def __init__(self, strategy_config: dict = None):
        super().__init__(
            strategy_name="MeanReversionStrategy", strategy_config=strategy_config
        )
        # Initialize parameters like lookback periods, deviation thresholds, etc.
        self.lookback_period = self.strategy_config.get("lookback_period", 20)
        self.std_dev_threshold = self.strategy_config.get("std_dev_threshold", 2.0)
        self.historical_performance = {"pnl": 0.0, "trades_executed": 0}  # Simplified

    def generate_signals(self, data: dict) -> list[dict]:
        """
        Generates trading signals based on mean reversion logic.
        Args:
            data (dict): Expected to contain historical price data for symbols.
                         Example: {'AAPL': {'prices': [150, 151, ..., 145], 'current_price': 145},
                                   'MSFT': {'prices': [...], 'current_price': ...}}
        Returns:
            list[dict]: A list of trading signals.
        """
        signals = []
        # In a real implementation, this would involve:
        # 1. Calculating historical mean and standard deviation for each symbol.
        # 2. Comparing current price to these statistical measures.
        # 3. Generating BUY signal if price is significantly below mean,
        #    SELL signal if significantly above.

        for symbol, symbol_data in data.items():
            prices = symbol_data.get("prices", [])
            current_price = symbol_data.get("current_price")

            if (
                not prices
                or current_price is None
                or len(prices) < self.lookback_period
            ):
                continue

            # Simplified calculation (using only the last `lookback_period` prices)
            relevant_prices = prices[-self.lookback_period :]
            mean_price = sum(relevant_prices) / len(relevant_prices)
            std_dev = (
                sum([(p - mean_price) ** 2 for p in relevant_prices])
                / len(relevant_prices)
            ) ** 0.5

            if std_dev == 0:  # Avoid division by zero or issues with flat prices
                continue

            z_score = (current_price - mean_price) / std_dev

            if z_score < -self.std_dev_threshold:  # Price is significantly below mean
                signals.append(
                    {
                        "symbol": symbol,
                        "action": "BUY",
                        "quantity": 10,  # Example quantity
                        "reason": f"Price {current_price} is {-z_score:.2f} std devs below mean {mean_price:.2f}",
                    }
                )
                self.historical_performance["pnl"] += 10  # mock P&L
                self.historical_performance["trades_executed"] += 1
            elif z_score > self.std_dev_threshold:  # Price is significantly above mean
                signals.append(
                    {
                        "symbol": symbol,
                        "action": "SELL",
                        "quantity": 10,  # Example quantity
                        "reason": f"Price {current_price} is {z_score:.2f} std devs above mean {mean_price:.2f}",
                    }
                )
                self.historical_performance[
                    "pnl"
                ] -= 5  # mock P&L (assuming short sell profit if price drops)
                self.historical_performance["trades_executed"] += 1

        return signals

    def get_performance(self) -> dict:
        """
        Reports the performance of the mean reversion strategy.
        Returns:
            dict: A dictionary containing performance metrics.
        """
        return self.historical_performance


if __name__ == "__main__":
    mr_config = {"lookback_period": 50, "std_dev_threshold": 2.5}
    mr_strategy = MeanReversionStrategy(strategy_config=mr_config)
    print(f"Strategy Name: {mr_strategy.get_name()}")

    # Example data
    market_data = {
        "AAPL": {
            "prices": [150, 151, 152, 153, 150, 148, 147, 145, 146, 144] * 5,  # 50 days
            "current_price": 130,  # Significantly below recent prices
        },
        "MSFT": {
            "prices": [200, 201, 202, 203, 204, 205, 206, 207, 208, 209] * 5,  # 50 days
            "current_price": 220,  # Significantly above recent prices
        },
        "GOOG": {
            "prices": [1000, 1001, 1000, 1001, 1000, 1001, 1000, 1001, 1000, 1001]
            * 5,  # 50 days
            "current_price": 1000.5,  # Close to mean
        },
    }
    generated_signals = mr_strategy.generate_signals(market_data)
    print(f"Generated Signals: {generated_signals}")
    print(f"Performance: {mr_strategy.get_performance()}")

    market_data_2 = {
        "AAPL": {
            "prices": ([150, 151, 152, 153, 150, 148, 147, 145, 146, 144] * 5) + [130],
            "current_price": 160,  # Reverted and overshot
        }
    }
    generated_signals_2 = mr_strategy.generate_signals(market_data_2)
    print(f"Generated Signals 2: {generated_signals_2}")
    print(f"Performance after 2nd batch: {mr_strategy.get_performance()}")
