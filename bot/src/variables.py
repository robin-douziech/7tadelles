import os

members_file = "json/members.json"

if os.getenv('BOT_ENV') == "PROD" :
	bot_guild_id = 1003249512577515590
else :
	bot_guild_id = 1099428860514271282

bot_owner_id = 394185214479302656


help_msg = """
Bonjour ! Je suis 7tadellesBot. Voici ce que je peux faire pour toi :
- **!help** : affiche ce message d'aide
- **!link <pseudo>** : lie ton compte discord à ton compte sur 7tadelles.com
"""