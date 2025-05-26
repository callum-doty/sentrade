from app.brokerage_interface.adaptors.alpaca_adaptor import place_market_order

def process_trading_signals_for_execution(signals: list[dict]):
    """Takes a list of trading signals and attempts to execute them using Alpaca."""
    for signal in signals:
        if signal['action'] == 'BUY':
            symbol = signal['symbol']
            # Assuming a fixed quantity and time in force for simplicity
            qty = 1
            time_in_force = 'ioc'  # Immediate Or Cancel
            place_market_order(symbol, qty, 'buy', time_in_force)
