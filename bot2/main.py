import discord, os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(
	command_prefix="!",
	intents=discord.Intents.all(),
)

@bot.event
async def on_ready() :
	print('bot is ready !')

class InviteButton(discord.ui.View) :

	def __init__(self, *args, **kwargs) :
		super(InviteButton, self).__init__()

		options = [
			discord.SelectOption(label="Option1", value="option1"),
			discord.SelectOption(label="Option2", value="option2"),
			discord.SelectOption(label="Option3", value="option3"),
		]

		self.add_item(discord.ui.Select(options=options))






@bot.command()
async def invite(ctx) :
	await ctx.send("Click the button below to invite someone !", view=InviteButton())




bot.run(os.getenv('TOKEN'))
