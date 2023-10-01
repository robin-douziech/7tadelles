import logging, json
from interactions import Client, Intents

from variables import *

logging.basicConfig()
cls_log = logging.getLogger("MyLogger")
cls_log.setLevel(logging.INFO)

class SeptTadellesBot(Client):

	def __init__(self, members_file, *args, **kwargs):
		super(SeptTadellesBot, self).__init__(
			intents=Intents.ALL,
			sync_interactions=True,
			asyncio_debug=True,
			logger=cls_log
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
