import logging, os, json
from dotenv import load_dotenv

from interactions import Client, Intents, listen
from interactions.api.events import Component
from interactions.ext import prefixed_commands

from interactions import slash_command, slash_option, SlashContext, context_menu, CommandType, Button, ActionRow, ButtonStyle, Extension, SelectMenu, SelectOption

from SeptTadellesBot import *

load_dotenv()

bot = SeptTadellesBot(members_file)
prefixed_commands.setup(bot)

@listen()
async def on_ready():

    bot.bot_guild = bot.get_guild(bot_guild_id)
    
    # liste des membres non bot du serveur
    guild_members = []
    for member in bot.bot_guild.members :
        if not(member.bot) :
            guild_members.append(f"{member}")

    with open(bot.members_file, "rt") as f :
        bot.members = json.load(f)

    # ajout des membres arrivés pendant que le bot était éteint
    for member in guild_members :
        if member not in bot.members :
            bot.members[member] = {
            }

    # suppression des membres partis pendant que le bot était éteint
    members_to_remove = []
    for member in bot.members :
        if member not in guild_members :
            members_to_remove.append(member)
    for member in members_to_remove :
        bot.members.pop(member)

    bot.write_json(bot.members, bot.members_file)
    
    print("Ready")
    print(f"This bot is owned by {bot.owner}")

@slash_command("help")
async def help_7tadellesbot(ctx: SlashContext) :
    button = Button(
        style=ButtonStyle.PRIMARY,
        custom_id='button',
        label="help button",
    )
    dm_channel = await ctx.author.fetch_dm()
    if ctx.channel_id == dm_channel.id :
        await ctx.send(help_msg, components=button)

@slash_command(
    name="score",
    description="Displays user's score on 7tadelles",
)
async def score_7tadellesbot(ctx) :
    select_menu = SelectMenu(
        custom_id = "select-menu",
        options = [
            SelectOption(label = "Option 1", value = "option1"),
            SelectOption(label = "Option 2", value = "option2"),
            SelectOption(label = "Option 3", value = "option3"),
        ],
        placeholder = "Select a game",
        min_value = 1,
        max_value = 1,
    )
    await ctx.send("Quel score voulez-vous voir ?", components=select_menu)



#bot.load_extension("test_components")
#bot.load_extension("test_application_commands")
bot.start(os.getenv('TOKEN'))