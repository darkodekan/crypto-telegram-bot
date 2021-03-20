# Crypto Telegram Bot

## Using

You can find the bot on Telegram. Bot username is @evil_chatbot and you can freely use it.
Bear in mind that bot is still in early stage of development so there may be a lot bugs.  

## Commands

Commands: 
- /p COIN - current price for the coin 
- /p COIN DATE - price for specific date in dd/mm/yy format(ex. 02/03/11).
For current year you can use dd/mm format.
- /h COIN DAYS - historical price graph for last amount of days
- /f - price for favorite coins
- /s COIN - save a coin to favorites
- /d COIN - delete a coin from favorites
- /cc CURRENCY - change currency(EUR, USD, GBP..) use international standard three letter code.

Developer: @darko_dekan on Telegram

## Running and configuration

If you wish to deploy the bot on your PC or virtual private server you need to configure the bot 
with config.py file.
Go to terminal and run:
python3 bot.py

If you want to deploy it on on a web server with Flask module(such as PythonAnywhere)
set WEB_SERVER in config.py to True.



## Future

- unit or/and integrations tests to be implemented
- /mc multiple prices option
- fixing formatting currency
- getting graph within certain time interval(/h eth 02/03/2011 02/03/2021)
- add .gitignore and remove pycache and other files
- notifications for rise or drop
- notify feature
- append link to end
- add database path in config
- create flask app only if explicitly said so
- more verbose info about coins
- get chat ids in admin feature
- api keys
- get database file
- apply decorators for repetitive tasks(for protected commands)
- format code to follow pep8 style guide
- code refactorization
- matplotlib figure closing
- fix title not showing on graph
- add to graph legends
- graph dates for larger data to be more sparse
- add commands to botfather
- add synonyms
- overlapping graphs
- fix error output date
- add possibility of year 2020
- add multiple formats
- set month locator
- gets stuck for multiple dates 
- subcribe to receive notification prices
- set weeks or days if less than
- list of coins
- fix bug finding min and max
- delete button
## License

Read the UNLICENSE file.