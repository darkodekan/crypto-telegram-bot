import cryptocompare
import graph
import telebot
import config
import os
from datetime import datetime
from flask import Flask, request #optional
from telebot import apihelper
from sqla_wrapper import SQLAlchemy


apihelper.ENABLE_MIDDLEWARE = True #  Not used atm

bot = telebot.TeleBot(config.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=config.WEBHOOK)

app = Flask(__name__)

db = SQLAlchemy("sqlite:///database.sqlite3")


class FavoriteCoin(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chat_id = db.Column(db.String)
    coin_symbol = db.Column(db.String)


db.create_all()


def send_historical_graph(chat_id, coin, days):
	list_of_prices = cryptocompare.get_historical_price_day(
		coin, config.CURRENCY, limit=days)
	if not list_of_prices:
		bot.send_message(chat_id, "No data for that time period.\
			Try shorter amount of days.")
		return

	dates = [datetime.utcfromtimestamp(price["time"])
			 for price in list_of_prices]
	prices = [price["open"] for price in list_of_prices]
	img_path = f"{chat_id}.jpg"

	graph.plot_graph(coin, dates, prices, img_path)
	with open(img_path, "rb") as img:
		bot.send_photo(chat_id, photo=img)
	os.remove(img_path)


#not necessary if not receiving webhooks, you can run just with
#bot.polling()
@app.route('/'+config.SECRET, methods=['POST'])
def webhook():
	update = telebot.types.Update.de_json(
		request.stream.read().decode('utf-8'))
	bot.process_new_updates([update])
	return 'ok', 200



@bot.middleware_handler(update_types=['message'])
def intercept_message(bot_instance, message):
	pass #  Implement saving user to database


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, config.START)


@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id, config.HELP)


@bot.message_handler(commands=['id'])
def get_chat_id(m):
	chat_id = m.chat.id
	message = "Chat id is: f{m.chat.id}"
	bot.send_message(m.chat.id, message)


@bot.message_handler(commands=['p'])
def get_coin_price(m):
	try:
		coin_symbol = m.text.split()[1].strip().upper()
		coin_data = cryptocompare.get_price(coin_symbol, config.CURRENCY)
		if coin_data:
			coin_price = coin_data[coin_symbol][config.CURRENCY]
			bot.send_message(m.chat.id, f'{coin_price}$')
		else:
			bot.send_message(m.chat.id, "Error: No such coin in database.")
	except IndexError:
		bot.send_message(m.chat.id, "Error: You need to specify coin symbol.\
			Example: /p eth")
	

@bot.message_handler(commands=['h'])
def get_historical_price_graph(m):
	try:
		text_commands = m.text.split()[1:]
		coin, days = text_commands
		days = int(days)
	except ValueError:
		bot.send_message(m.chat.id, f"Error: You need to pass coin symbol and days.")
	else:
		coin_data = cryptocompare.get_price(coin, config.CURRENCY)
		if coin_data:
			send_historical_graph(m.chat.id, coin, days)
		else:
			bot.send_message(m.chat.id, f"No data for such coin.")


@bot.message_handler(commands=['s'])
def save_favorite_coin(m):
	try:
		coin = m.text.split()[1].strip().upper()
	except IndexError:
		bot.send_message(m.chat.id, "You need to provide coin symbol.")
	else:
		coin_price = cryptocompare.get_price(coin, config.CURRENCY)
		if coin_price is None:
			bot.send_message(m.chat.id, "No such coin in database.")
		elif FavoriteCoin.exists(coin_symbol=coin):
			bot.send_message(m.chat.id, "Coin is already saved!")
		else:
			favorite_coin = FavoriteCoin(chat_id=m.chat.id, coin_symbol=coin)
			favorite_coin.save()
			bot.send_message(m.chat.id, "Added new coin!")


@bot.message_handler(commands=['d'])
def delete_favorite_coin(m):
	try:
		coin = m.text.split()[1].strip().upper()
		favorite_coin = FavoriteCoin.first(coin_symbol=coin)
		if favorite_coin:
			favorite_coin.delete()
			bot.send_message(m.chat.id, "Removed a coin!")
		else:
			bot.send_message(m.chat.id, "Coin doesn't exist in favorites.")
	except IndexError:
		bot.send_message(m.chat.id, "Error: You need to provide symbol name.")


@bot.message_handler(commands=['f'])
def get_favorites(m):
	coins = [favorite_coin.coin_symbol 
			 for favorite_coin in db.query(FavoriteCoin).filter_by(chat_id=m.chat.id)]
	if not coins:
		bot.send_message(m.chat.id, "You don't have any coins in favorites.")
	else:
		cryptos = cryptocompare.get_price(coins, [config.CURRENCY])
		if cryptos:
			formatted_message = "\n".join(f"{crypto}: {cryptos[crypto][config.CURRENCY]}$" 
											for crypto in cryptos)
			bot.send_message(m.chat.id, formatted_message)
		else:
			bot.send_message(m.chat.id, "No results.")


if __name__ == "__main__":
	bot.remove_webhook()
	bot.polling()
	#app.run() use this when running flask app
