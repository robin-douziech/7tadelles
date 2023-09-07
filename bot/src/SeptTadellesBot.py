from discord.ext import commands
import discord, json

from variables import *

class SeptTadellesBot(commands.Bot) :

	def __init__(self, members_file) :
		super().__init__(command_prefix="!", intents=discord.Intents.all())

		self.members_file = members_file
		self.members = {}

		self.bot_guild = None

	def write_json(self, dic, file) :
		json_object = json.dumps(dic, indent=2)
		with open(file, "wt") as f :
			f.write(json_object)

	def fetch_member(self, pseudo) :
		for member in self.bot_guild.members :
			if pseudo == f"{member.name}#{member.discriminator}" :
				return member
		return None

	async def verify_user(self, username, link) :

		print(f"discord_username : {username}")

		if username in self.members :

			print("okok")

			await self.fetch_member(username).dm_channel.send(f"Voici un lien pour lier votre compte discord : {link}")

