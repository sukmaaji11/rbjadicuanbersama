import pandas as pd

class ICTStrategy:
    def __init__(self):
        self.risk_per_trade = 0.02  # 2% risk
        
    def analyze(self, df):
        """Simplified ICT-inspired strategy"""
        try:
            # Detect FVG
            df['fvg_bullish'] = (df['low'].shift(1) > df['high'].shift(3)).astype(int)
            
            # Detect Order Blocks
            df['volatility'] = (df['high'] - df['low']).rolling(5).mean()
            df['order_block'] = (df['volatility'] < df['volatility'].quantile(0.2)).astype(int)
            
            # Generate signals
            df['signal'] = 0
            df.loc[(df['fvg_bullish'] == 1) & (df['order_block'] == 1), 'signal'] = 1
            
            return df
        except Exception as e:
            raise RuntimeError(f"Strategy analysis failed: {str(e)}")