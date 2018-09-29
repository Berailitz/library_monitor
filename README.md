# BUPT Library Monitor

Monitor books in BUPT's library, send telegram messages if they become avaiable.

### Features
 - Support multiply users
 - Multiply notifications for each book
 - Support multiply locations
 - Platform independent
 - Custom text template
 - Embeded message queued
 - Proxy support
 - Support JSON database
 - No SQL server needed

### Requirements
 - A Telegram bot account
 - Python 3.6 or above
 - Packages in `requirements.txt`
 - Pyenv (recommend)

### Installation
1. Talk to [BotFather](https://telegram.me/BotFather) and create a bot.
1. Create a [pyenv](https://github.com/pyenv/pyenv) enviroment (recommend).
1. Install dependencies.
1. Copy `config.default.py` to `config.py`.
1. Copy `database.default` to `database`.
1. Edit `config.py` and `database/*.json`.
1. Run `python3 install.py`.
1. Run `python3 run.py`.
