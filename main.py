import time
import pandas as pd
from utils.exchange import get_testnet_exchange
from utils.logger import setup_logger
from strategies.ict_strategy import ICTStrategy

logger = setup_logger()
exchange = get_testnet_exchange()
exchange.set_sandbox_mode(True)
strategy = ICTStrategy()

def fetch_data(symbol='BTC/USDT', timeframe='15m', limit=100):
    """Fetch OHLCV data from Testnet"""
    try:
        data = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        print("Connected!")
        return df.set_index('timestamp')
    except Exception as e:
        logger.error(f"Data fetch failed: {str(e)}")
        return None

def execute_trade(symbol, signal):
    """Execute trade with risk management"""
    try:
        balance = exchange.fetch_balance()['USDT']['free']
        price = exchange.fetch_ticker(symbol)['last']
        
        if signal == 1:  # Buy
            amount = (balance * strategy.risk_per_trade) / price
            order = exchange.create_market_buy_order(symbol, amount)
            logger.info(f"BUY Order Executed: {order}")
        elif signal == -1:  # Sell
            amount = exchange.fetch_balance()[symbol.split('/')[0]]['free']
            order = exchange.create_market_sell_order(symbol, amount)
            logger.info(f"SELL Order Executed: {order}")
    except Exception as e:
        logger.error(f"Trade execution failed: {str(e)}")

def run_bot():
    logger.info("Starting Testnet Trading Bot")
    while True:
        try:
            df = fetch_data()
            if df is not None:
                df = strategy.analyze(df)
                latest_signal = df['signal'].iloc[-1]
                
                if latest_signal != 0:
                    execute_trade('BTC/USDT', latest_signal)
                    
            time.sleep(60)  # Run every minute
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"Main loop error: {str(e)}")
            time.sleep(60)

if __name__ == "__main__":
    run_bot()