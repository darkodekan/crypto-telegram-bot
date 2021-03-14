import os
START = "Hello! I am Evil Bot. Type /help if you want to see all the commands for me."
HELP = """Commands: 
/p <COIN> - current price for the coin 
/h <COIN> <DAYS> - historical price graph
/f - price for favorite coins
/s <COIN> - save a coin to favorites
/d <COIN> - delete a coin from favorites
"""
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SECRET = os.environ["WEBHOOK_SECRET"]
WEBHOOK = f'{os.environ["WEBHOOK_URL"]}/{SECRET}'
CURRENCY = "USD"
