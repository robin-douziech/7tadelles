from dotenv import load_dotenv
import os

from bot import *

load_dotenv()

bot.remove_command('help')
bot.run(os.getenv('TOKEN'))