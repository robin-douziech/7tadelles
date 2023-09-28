import discord, os, requests
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

class ClassementSelect(discord.ui.Select) :

	def __init__(self, bot, *args, **kwargs) :
		super(ClassementSelect, self).__init__(*args, **kwargs)
		self.bot = bot

	async def callback(self, interaction: discord.Interaction) :
		user = interaction.user
		if os.getenv('SITE_ENV') == "PROD" :
			url = f"https://7tadelles.com/account/bot/get-classement/{os.getenv('TOKEN')}?game={self.values[0]}"
		else :
			url = f"http://127.0.0.1:8000/account/bot/get-classement/{os.getenv('TOKEN')}?game={self.values[0]}"
		response = requests.get(url).json()['data']
		position = [':first_place:', ':second_place:', ':third_place:', *[i for i in range(4, len(response['classement'])+1)]]
		if response['result'] == "success" :
			if self.values[0] == "Général" :
				msg = "Classement général :\n"
				await self.bot.change_presence(activity=discord.CustomActivity(f"\\:first_place: {response['classement'][0][0]}"))
			else :
				msg = f"Classement du jeu \"{self.values[0]}\" :\n"
			for i,line in enumerate(response['classement']) :
				msg += f"{position[i]} {line[0]} ({line[1]} points)\n"
			await interaction.response.send_message(msg, ephemeral=False)


class ScoreSelect(discord.ui.Select) :

	def __init__(self, *args, **kwargs) :
		super(ScoreSelect, self).__init__(*args, **kwargs)

	async def callback(self, interaction: discord.Interaction) :
		user = interaction.user
		if os.getenv('SITE_ENV') == "PROD" :
			url = f"https://7tadelles.com/account/bot/get-score/{os.getenv('TOKEN')}?game={self.values[0]}&id={user.id}"
		else :
			url = f"http://127.0.0.1:8000/account/bot/get-score/{os.getenv('TOKEN')}?game={self.values[0]}&id={user.id}"
		response = requests.get(url).json()['data']
		if response['result'] == "success" :
			if self.values[0] == "Général" :
				await interaction.response.send_message(f"Voici votre score au classement général : **{response['score']}**", ephemeral=False)
			else :
				await interaction.response.send_message(f"Voici votre score au jeu \"{self.values[0]}\" : **{response['score']}**", ephemeral=False)
		elif response['result'] == "failure" and 'error_msg' in response.keys() :
			await interaction.response.send_message(f"Une erreur est intervenue lors de ma requête à 7tadelles.com : {response['error_msg']}", ephemeral=True)



class ClassementSelectView(discord.ui.View) :

	def __init__(self, bot, options, *args, **kwargs) :
		super(ClassementSelectView, self).__init__(*args, **kwargs)
		self.add_item(ClassementSelect(
			bot,
			options=options,
			placeholder="Sélectionnez un jeu",
			custom_id="select-game",
		))


class ScoreSelectView(discord.ui.View) :

	def __init__(self, options, *args, **kwargs) :
		super(ScoreSelectView, self).__init__(*args, **kwargs)
		self.add_item(ScoreSelect(
			options=options,
			placeholder="Sélectionnez un jeu",
			custom_id="select-game",
		))