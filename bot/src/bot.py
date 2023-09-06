from discord.ext import tasks, commands
import json

from SeptTadellesBot import *

bot = SeptTadellesBot(members_file)

@bot.event
async def on_ready() :

	bot.bot_guild = bot.get_guild(bot_guild_id)

	# liste des membres non bot du serveur
	guild_members = []
	for member in bot.bot_guild.members :
		if not(member.bot) :
			guild_members.append(member)
			if member.dm_channel == None :
				await member.create_dm()

	with open(bot.members_file, "rt") as f :
		bot.members = json.load(f)

	# ajout des membres arrivés pendant que le bot était éteint
	for member in guild_members :
		if member not in bot.members :
			bot.members[member] = {
				"name" : member.split('#')[0],
				"id"   : member.split('#')[1]
			}

	# suppression des membres partis pendant que le bot était éteint
	members_to_remove = []
	for member in bot.members :
		if member not in guild_members :
			members_to_remove.append(member)
	for member in members_to_remove :
		bot.members.pop(member)

	bot.write_json(bot.members, bot.members_file)

	print(f"{bot.user.display_name} est prêt.")