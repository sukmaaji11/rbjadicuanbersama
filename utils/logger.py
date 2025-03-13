import logging
import os
from datetime import datetime

def setup_logger():
    if not os.path.exists('logs'):
        os.makedirs('logs')

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(message)s', 
            handlers=[logging.FileHandler(f'logs/trading_{datetime.now().strftime("%Y%m%d")}.log'),logging.StreamHandler()]
        )

    return logging.getLogger(__name__)