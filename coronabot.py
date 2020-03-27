import logging
import handlers

from telegram.ext import Updater
from telegram.ext import CommandHandler

# Create an updater
updater = Updater(token='TOKEN', use_context=True)

# Expose the dispatcher locally
dispatcher = updater.dispatcher

# Configure warning level logging.
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)

# Create a list of all handlers
handlers = {
    "start": handlers.start_handler,
    "help" : handlers.help_handler,
    "countries" : handlers.countries_handler,
    "summary" : handlers.summary_handler,
    "confirmed" : handlers.confirmed_handler,
    "recovered" : handlers.recovered_handler,
    "deaths" : handlers.deaths_handler,
    "stats": handlers.stats_handler
}

# Add all handlers to the dispatcher
for handler_name in handlers:
    dispatcher.add_handler(CommandHandler(handler_name, handlers[handler_name]))

# Start the bot
updater.start_polling()