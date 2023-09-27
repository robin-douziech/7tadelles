from discord.ext import commands
import discord, json, logging

from variables import *

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    filename='bot.log',
    format='[%(asctime)s] %(levelname)s - %(message)s',  
    datefmt='%Y-%m-%d %H:%M:%S'  
)

class SeptTadellesBot(commands.Bot) :

	def __init__(self, members_file) :

		intents = discord.Intents.all()
		intents.message_content = True
		super().__init__(
			command_prefix="!",
			intents=intents,
			activity=discord.Game("shifumi avec GameBot")
		)

		self.members_file = members_file
		self.members = {}

		self.bot_guild = None

	def log(self, message) :
		logging.info(message)

	def write_json(self, dic, file) :
		json_object = json.dumps(dic, indent=2)
		with open(file, "wt") as f :
			f.write(json_object)

	def fetch_member(self, pseudo) :
		for member in self.bot_guild.members :
			if pseudo == f"{member.name}#{member.discriminator}" :
				return member
		return None

	