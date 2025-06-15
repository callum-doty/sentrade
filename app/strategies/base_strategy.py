# app/strategies/base_strategy.py
from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """
    Abstract base class for all trading strategies.
    Each strategy must implement methods to generate signals
    and to report its performance.
    """

    def __init__(self, strategy_name: str, strategy_config: dict = None):
        """
        Initializes the base strategy.
        Args:
            strategy_name (str): The unique name of the strategy.
            strategy_config (dict, optional): Configuration parameters for the strategy.
        """
        self.strategy_name = strategy_name
        self.strategy_config = strategy_config if strategy_config else {}

    @abstractmethod
    def generate_signals(self, data: dict) -> list[dict]:
        """
        Generates trading signals based on the input data.
        Args:
            data (dict): A dictionary containing the necessary data for the strategy
                         (e.g., market data, features).
        Returns:
            list[dict]: A list of trading signals. Each signal should be a dictionary
                        containing details like 'symbol', 'action' (BUY/SELL), 'quantity',
                        'price_target', 'stop_loss', etc.
        """
        pass

    @abstractmethod
    def get_performance(self) -> dict:
        """
        Reports the performance of the strategy.
        This could include P&L, Sharpe ratio, win rate, etc.
        The specific metrics will be used by the EWAAllocator.
        Returns:
            dict: A dictionary containing performance metrics for the strategy.
        """
        pass

    def get_name(self) -> str:
        """
        Returns the name of the strategy.
        """
        return self.strategy_name


if __name__ == "__main__":
    # This is an abstract class and cannot be instantiated directly.
    # Example of how a concrete strategy might inherit from it:

    class MyConcreteStrategy(BaseStrategy):
        def __init__(self, strategy_config: dict = None):
            super().__init__(
                strategy_name="MyConcreteStrategy", strategy_config=strategy_config
            )
            self.trades_pnl = []  # Simplified P&L tracking

        def generate_signals(self, data: dict) -> list[dict]:
            signals = []
            # Example: Buy AAPL if some condition in data is met
            if data.get("AAPL_price", 0) < 150:
                signals.append(
                    {
                        "symbol": "AAPL",
                        "action": "BUY",
                        "quantity": 10,
                        "reason": "Price below $150",
                    }
                )
            # Simulate some P&L for this signal if executed
            self.trades_pnl.append(
                data.get("AAPL_price_change", 0.01) * 10
            )  # Simplified
            return signals

        def get_performance(self) -> dict:
            # Example: Calculate total P&L
            total_pnl = sum(self.trades_pnl)
            return {"pnl": total_pnl, "trades_count": len(self.trades_pnl)}

    # Instantiate and use the concrete strategy
    my_strategy_config = {"some_param": "value"}
    my_strategy = MyConcreteStrategy(strategy_config=my_strategy_config)
    print(f"Strategy Name: {my_strategy.get_name()}")

    # Simulate some data
    market_data_period_1 = {
        "AAPL_price": 145,
        "AAPL_price_change": 0.02,
    }  # Price went up 2%
    signals_1 = my_strategy.generate_signals(market_data_period_1)
    print(f"Signals (Period 1): {signals_1}")
    print(f"Performance (Period 1): {my_strategy.get_performance()}")

    market_data_period_2 = {
        "AAPL_price": 155,
        "AAPL_price_change": -0.01,
    }  # Price went down 1%
    signals_2 = my_strategy.generate_signals(
        market_data_period_2
    )  # No signal generated
    print(f"Signals (Period 2): {signals_2}")
    print(
        f"Performance (Period 2): {my_strategy.get_performance()}"
    )  # P&L includes previous trade
