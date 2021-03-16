import os

START = """Hello! I am Evil Bot. I keep track of cryptocurrency prices of thousand coins. 
Type /help if you want to see all the commands for me.
I use Cryptocompare API to fetch data.
I'm still in early stage of development, there may be mainteinance periods
when I am down.

If you encounter any bugs or have any feature requests, open an issue in official github repository:
https://github.com/darkodekan/crypto-telegram-bot
Developer: @darko_dekan on Telegram"""

HELP = """Commands: 
/p COIN - current price for the coin(use standard symbol code such as BTC, ETH, LTC, DOGE...)
/p COIN DATE - price for specific date in dd/mm/yy format(ex. 02/03/11).
For current year you can use dd/mm format.
/h COIN DAYS - historical price graph for last amount of days
/f - price for favorite coins
/s COIN - save a coin to favorites
/d COIN - delete a coin from favorites
/cc CURRENCY - change currency(EUR, USD, GBP..) use internatoinal standard three letter code.

If you encounter any bugs or have any feature requests, open an issue in official github repository:
https://github.com/darkodekan/crypto-telegram-bot

Developer: @darko_dekan on Telegram
"""

PRIVACY = """Your personal data such as Telegram name or username is not stored in database.
Only chat_id and favorite coins associated with that chat. Soon there will be option to 
delete all data."""

DATABASE_PATH = "sqlite:///database.sqlite3"

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

WEBHOOK = "" #if using as a web server you need to set webhook(url to web server)

WEB_SERVER = False # dont forget to set webhook url

CURRENCY = "USD"

ADMINS = ["darko_dekan"] #telegram usernames assigned as admins