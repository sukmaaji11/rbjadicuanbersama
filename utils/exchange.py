import ccxt
import os
from dotenv import load_dotenv
from .logger import setup_logger

logger = setup_logger()

def get_testnet_exchange():
    load_dotenv()
    
    return ccxt.binance({
        'apiKey': os.getenv("TESTNET_API_KEY"),
        'secret': os.getenv("TESTNET_API_SECRET"),
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
            'adjustForTimeDifference': True
        },
        'urls': {
            'api': 'https://testnet.binance.vision/api'
        }
    })