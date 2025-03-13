from utils.exchange import get_testnet_exchange


exchange = get_testnet_exchange()
exchange.set_sandbox_mode(True)

balance = exchange.fetch_balance()
print("Testnet Balance:", balance["USDT"])