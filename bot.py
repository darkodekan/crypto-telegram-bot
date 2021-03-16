import cryptocompare
import graph
import telebot
import config
import os
import currency
from datetime import datetime
from telebot import apihelper, types
from telebot.apihelper import ApiTelegramException
from sqla_wrapper import SQLAlchemy

apihelper.ENABLE_MIDDLEWARE = True #  Not used atm

bot = telebot.TeleBot(config.TOKEN, threaded=False)

if config.WEB_SERVER:
	from flask import Flask, request
	bot.remove_webhook()
	bot.set_webhook(url=config.WEBHOOK)
	app = Flask(__name__)

db = SQLAlchemy(config.DATABASE_PATH)




class Chat(db.Model):
	__tablename__ = "chat"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	telegram_chat_id = db.Column(db.Integer, unique=True, nullable=False)
	currency_code = db.Column(db.String(3), nullable=False, default="USD")
	favorite_coins = db.relationship('FavoriteCoin', backref='chat')

class FavoriteCoin(db.Model):
	__tablename__ = "favorite_coin"
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	coin_symbol = db.Column(db.String, nullable=False)
	chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'))



db.create_all()


def send_historical_graph(chat, coin, days):
	list_of_prices = cryptocompare.get_historical_price_day(
		coin, chat.currency_code, limit=days)
	if not list_of_prices:
		bot.send_message(chat.telegram_chat_id, "No data for that time period.\
			Try shorter amount of days.")
		return

	dates = [datetime.utcfromtimestamp(price["time"])
			 for price in list_of_prices]
	prices = [price["open"] for price in list_of_prices]
	img_path = f"{chat.telegram_chat_id}.jpg"

	graph.plot_graph(coin, dates, prices, img_path)
	with open(img_path, "rb") as img:
		bot.send_photo(chat.telegram_chat_id, photo=img)
	os.remove(img_path)


if config.WEB_SERVER:
	@app.route('/'+config.SECRET, methods=['POST'])
	def webhook():
		update = telebot.types.Update.de_json(
			request.stream.read().decode('utf-8'))
		bot.process_new_updates([update])
		return 'ok', 200



@bot.middleware_handler(update_types=['message'])
def intercept_message(bot_instance, message):
	telegram_chat_id= message.chat.id
	chat = Chat.create_or_first(telegram_chat_id=telegram_chat_id)
	if chat:
		pass


@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, config.START)


@bot.message_handler(commands=['help'])
def help(m):
    bot.send_message(m.chat.id, config.HELP)


@bot.message_handler(commands=['id'])
def get_chat_id(m):
	chat_id = m.chat.id
	message = f"Chat id is: f{chat_id}"
	bot.send_message(m.chat.id, message)


@bot.message_handler(commands=['p'])
def get_coin_price(m):
	chat = Chat.first(telegram_chat_id=m.chat.id)
	print(chat.currency_code)

	try:
		user_commands = m.text.split()
		coin_symbol = user_commands[1].upper()

		if len(user_commands) == 2: # /p eth
			coin_data = cryptocompare.get_price(coin_symbol, chat.currency_code)

		elif len(user_commands) == 3: # /p eth 02/03 or /p eth 02/03/45
			date_str = user_commands[2]
			num_slashes = date_str.count("/") 
			try:
				if num_slashes == 1:
					date = datetime.strptime(date_str, 
										     "%d/%m")
					current_year = datetime.now().year
					date = date.replace(year = current_year)
				elif num_slashes == 2:
					date = datetime.strptime(date_str, 
										     "%d/%m/%y")
				else:
					raise ValueError
			except ValueError:
				bot.send_message(m.chat.id, "Error: Wrong date format. Use dd/mm or dd/mm/yy.")
				return
			else:
				coin_data = cryptocompare.get_historical_price(coin_symbol, 
												               chat.currency_code, 
												               date)
		else:
			bot.send_message(m.chat.id, "Error: Excess number of arguments.\
				\nType /help to see available commands.")	
			return

		if coin_data:
			coin_price = coin_data[coin_symbol][chat.currency_code]
			formatted_price = currency.pretty(coin_price, chat.currency_code)
			bot.send_message(m.chat.id, formatted_price)
		else:
			bot.send_message(m.chat.id, f"{coin_symbol} doesn't exist in database. \
				Use codes for coins, not full names.")

	except IndexError:
		bot.send_message(m.chat.id, "Error: You need to specify coin symbol.\
			Example: /p eth")
	

@bot.message_handler(commands=['h'])
def get_historical_price_graph(m):
	chat = Chat.first(telegram_chat_id=m.chat.id)
	try:
		text_commands = m.text.split()[1:]
		coin, days = text_commands
		days = int(days)
	except ValueError:
		bot.send_message(m.chat.id, f"Error: You need to pass coin symbol and days.")
	else:
		coin_data = cryptocompare.get_price(coin, chat.currency_code)
		if coin_data:
			send_historical_graph(chat, coin, days)
		else:
			bot.send_message(m.chat.id, f"No data for such coin.")


@bot.message_handler(commands=['s'])
def save_favorite_coin(m):
	chat = Chat.first(telegram_chat_id=m.chat.id)
	currency = chat.currency_code
	try:
		coin = m.text.split()[1].strip().upper()
	except IndexError:
		bot.send_message(m.chat.id, "You need to provide coin symbol.")
	else:
		coin_price = cryptocompare.get_price(coin, currency)
		if coin_price is None:
			bot.send_message(m.chat.id, "No such coin in database.")
		elif FavoriteCoin.exists(chat=chat, coin_symbol=coin):
			bot.send_message(m.chat.id, "Coin is already saved!")
		else:
			favorite_coin = FavoriteCoin(chat=chat, coin_symbol=coin)
			favorite_coin.save()
			bot.send_message(m.chat.id, "Added new coin!")


@bot.message_handler(commands=['d'])
def delete_favorite_coin(m):
	chat = Chat.first(telegram_chat_id=m.chat.id)
	try:
		coin = m.text.split()[1].strip().upper()
		favorite_coin = FavoriteCoin.first(chat=chat, coin_symbol=coin)
		if favorite_coin:
			favorite_coin.delete()
			bot.send_message(m.chat.id, "Removed a coin!")
		else:
			bot.send_message(m.chat.id, "Coin doesn't exist in favorites.")
	except IndexError:
		bot.send_message(m.chat.id, "Error: You need to provide symbol name.")


@bot.message_handler(commands=['f'])
def get_favorites(m):
	chat = Chat.first(telegram_chat_id=m.chat.id)
	coins = [coin.coin_symbol for coin in chat.favorite_coins]

	if not coins:
		bot.send_message(m.chat.id, "You don't have any coins in favorites.")
	else:
		cryptos = cryptocompare.get_price(coins, [chat.currency_code])
		if cryptos:
			formatted_message = "\n".join(f"""{crypto}: {currency.pretty(cryptos[crypto][chat.currency_code], chat.currency_code)}"""
											for crypto in cryptos)
			bot.send_message(m.chat.id, formatted_message)
		else:
			bot.send_message(m.chat.id, "No results.")


@bot.message_handler(commands=['cc'])
def change_currency(m):
	chat = Chat.first(telegram_chat_id=m.chat.id)
	try:
		currency_code = m.text.split()[1].upper()
		currency.name(currency_code)
		chat.currency_code = currency_code
		chat.save()
		bot.send_message(m.chat.id, "New currency has been successfully set.")
	except IndexError:
		bot.send_message(m.chat.id, "You need to specify currency")
	except currency.exceptions.CurrencyException:
		bot.send_message(m.chat.id, "Invalid currency code.")


@bot.message_handler(commands=['notify'])
def notify_all(m):
	username = m.from_user.username
	if username in config.ADMINS:
		content = m.text.replace("/notify", "").strip()
		if not content:
			bot.send_message(m.chat.id, "Error: Message is empty")
			return 
		chats = db.query(Chat).all()
		for chat in chats:
			telegram_chat_id = chat.telegram_chat_id
			if telegram_chat_id != m.chat.id:
				bot.send_message(telegram_chat_id, content)


@bot.message_handler(commands=['chatids'])
def get_database(m):
	username = m.from_user.username
	if username in config.ADMINS:
		chats = db.query(Chat).all()
		if chats:
			message = "\n".join(str(chat.telegram_chat_id)
								for chat in chats)
			bot.send_message(m.chat.id, message)
		else:
			bot.send_message(m.chat.id, "No chats in database")



@bot.message_handler(commands=['notifyone'])
def notify_one(m):
	username = m.from_user.username
	if username in config.ADMINS:
		try:
			chat_id_and_content = m.text.replace("/notifyone", "").strip()
			chat_id = int(chat_id_and_content.split()[0])
			content = chat_id_and_content.replace(str(chat_id), "")
			bot.send_message(chat_id, content)

		except IndexError:
			bot.send_message(m.chat.id, "Incomplete arguments")
		
		except ValueError:
			bot.send_message(m.chat.id, "Id needs to be a number")

		except ApiTelegramException:
			bot.send_message(m.chat.id, "Wrong chat id")
		

if __name__ == "__main__":
	print("Bot is running...")
	if config.WEB_SERVER:
		app.run()
	else:
		bot.remove_webhook()
		bot.polling()
