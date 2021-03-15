import os
START = """Hello! I am Evil Bot. I keep track of cryptocurrency prices. 
Type /help if you want to see all the commands for me.
I use Cryptocompare API to fetch data.
I'm still in early stage of development, there may be mainteinance periods
when I am down.
If you encounter any bugs or have any feature requests, contact the developer at:
@darko_dekan"""

HELP = """Commands: 
/p COIN - current price for the coin 
/p COIN DATE - price for specific date in dd/mm/yy format(ex. 02/03/11).
For current year you can use dd/mm format.
/h COIN DAYS - historical price graph for last amount of days
/f - price for favorite coins
/s COIN - save a coin to favorites
/d COIN - delete a coin from favorites
/cc CURRENCY - change currency(EUR, USD, GBP..) use internatinal standard three letter code.
/mc - multiple prices

If you encounter any bugs or have any feature requests, open an issue of official github repository:
https://github.com/darkodekan/crypto-telegram-bot

Developer: @darko_dekan on Telegram
"""

PRIVACY = """Your personal data such as Telegram name or username is not stored in database.
Only chat_id and favorite coins associated with that chat."""

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

SECRET = ""

WEBHOOK = ""

CURRENCY = "USD"
