import discord, os, requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class ClassementSelect(discord.ui.Select) :

	def __init__(self, *args, **kwargs) :
		super(ClassementSelect, self).__init__(*args, **kwargs)

	async def callback(self, interaction: discord.Interaction) :
		user = interaction.user
		if os.getenv('SITE_ENV') == "PROD" :
			url = f"https://7tadelles.com/account/bot/get-classement/{os.getenv('TOKEN')}?game={self.values[0]}"
		else :
			url = f"http://127.0.0.1:8000/account/bot/get-classement/{os.getenv('TOKEN')}?game={self.values[0]}"
		response = requests.get(url).json()['data']
		position = [':first_place:', ':second_place:', ':third_place:', *[i for i in range(4, len(response['classement'])+1)]]
		if response['result'] == "success" :
			msg = ""
			for i,line in enumerate(response['classement']) :
				msg += f"{position[i]} {line[0]} ({line[1]} points)\n"
			await interaction.response.send_message(msg, ephemeral=True)


class ClassementSelectView(discord.ui.View) :

	def __init__(self, options, *args, **kwargs) :
		super(ClassementSelectView, self).__init__(*args, **kwargs)
		self.add_item(ClassementSelect(
			options=options,
			placeholder="Sélectionnez un jeu",
			custom_id="select-game",
		))

	