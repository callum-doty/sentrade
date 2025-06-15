# app/portfolio_manager/ewa_allocator.py


class EWAAllocator:
    """
    Exponentially Weighted Average (EWA) Allocator.
    Manages capital allocation to different trading strategies
    based on their historical performance.
    """

    def __init__(
        self,
        strategies: list[str],
        initial_weights: dict = None,
        learning_rate: float = 0.1,
    ):
        """
        Initializes the EWA Allocator.
        Args:
            strategies (list[str]): A list of strategy names.
            initial_weights (dict, optional): Initial weights for each strategy. Defaults to equal weighting.
            learning_rate (float, optional): The learning rate for updating weights. Defaults to 0.1.
        """
        self.strategies = strategies
        self.learning_rate = learning_rate
        if initial_weights:
            self.weights = initial_weights
        else:
            self.weights = {strategy: 1.0 / len(strategies) for strategy in strategies}

    def update_weights(self, strategy_performance: dict):
        """
        Updates the weights of the strategies based on their recent performance.
        Args:
            strategy_performance (dict): A dictionary where keys are strategy names
                                         and values are their performance metrics (e.g., P&L, Sharpe).
                                         Higher performance values are assumed to be better.
        """
        # This is a simplified update mechanism.
        # A more robust implementation would consider normalization, risk, etc.
        total_performance = sum(strategy_performance.values())

        if (
            total_performance == 0
        ):  # Avoid division by zero if all strategies had zero performance
            return

        for strategy in self.strategies:
            performance = strategy_performance.get(
                strategy, 0
            )  # Default to 0 if no performance data

            # Calculate the reward for the strategy
            reward = performance / total_performance if total_performance != 0 else 0

            # Update weight: w_t+1 = (1 - learning_rate) * w_t + learning_rate * reward
            current_weight = self.weights.get(strategy, 0)
            new_weight = (
                1 - self.learning_rate
            ) * current_weight + self.learning_rate * reward
            self.weights[strategy] = new_weight

        # Normalize weights to sum to 1
        self._normalize_weights()

    def _normalize_weights(self):
        """
        Normalizes the weights so that they sum to 1.
        """
        total_weight = sum(self.weights.values())
        if total_weight > 0:
            for strategy in self.weights:
                self.weights[strategy] /= total_weight
        else:
            # Fallback to equal weighting if total_weight is zero (e.g. all weights became zero)
            self.weights = {
                strategy: 1.0 / len(self.strategies) for strategy in self.strategies
            }

    def get_allocations(self) -> dict:
        """
        Returns the current capital allocation percentages for each strategy.
        Returns:
            dict: A dictionary where keys are strategy names and values are their
                  capital allocation percentages.
        """
        return self.weights


if __name__ == "__main__":
    # Example Usage
    strategies = ["SentimentStrategy", "MeanReversionStrategy", "MomentumStrategy"]
    allocator = EWAAllocator(strategies, learning_rate=0.1)

    print("Initial Allocations:", allocator.get_allocations())

    # Simulate some performance data (e.g., daily P&L)
    performance_period_1 = {
        "SentimentStrategy": 0.02,  # 2% gain
        "MeanReversionStrategy": -0.01,  # 1% loss
        "MomentumStrategy": 0.015,  # 1.5% gain
    }
    allocator.update_weights(performance_period_1)
    print("Allocations after Period 1:", allocator.get_allocations())

    performance_period_2 = {
        "SentimentStrategy": 0.03,
        "MeanReversionStrategy": 0.005,
        "MomentumStrategy": -0.005,
    }
    allocator.update_weights(performance_period_2)
    print("Allocations after Period 2:", allocator.get_allocations())

    performance_period_3 = {
        "SentimentStrategy": -0.01,
        "MeanReversionStrategy": 0.02,
        "MomentumStrategy": 0.025,
    }
    allocator.update_weights(performance_period_3)
    print("Allocations after Period 3:", allocator.get_allocations())
