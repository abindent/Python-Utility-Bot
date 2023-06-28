# IMPORTING THE PACKAGES
import os, json, nextcord, logging, datetime, random
from pathlib import Path
import motor.motor_asyncio
from nextcord.ext import commands
from dotenv import load_dotenv

# LOADING EXTENSIONS FROM UTILS
from utils import json_loader
from utils.delbtn import DelBtnSlashInteractionCheck, DelBtn
from utils.mongo import Document
from utils.config_db import Blacklist_DB


# CONFIGURATIONS
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-------")

# LOADING ENVIRONMENT VARIABLES
load_dotenv()

# GETTING PREFIX FROM DATABASE
async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("t!")(bot, message)

    try:
        data = await client.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or("t!")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or("t!")(bot, message)


# Changing Bot Presense
activity = nextcord.Game(name=f"Please interact with  me!")

# Intents
intents = nextcord.Intents.default()
intents.members = True
    
# OUR CLIENT     
client = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, activity=activity, intents=intents)




client.config_token = os.getenv("BOT_TOKEN")
client.connection_url = os.getenv("MONGO_URI")
client.guild_id="932264473408966656"
logging.basicConfig(level=logging.INFO)


client.muted_users = {}
client.cwd = cwd

client.version = "4.0.1alpha"

client.colors = {
    "WHITE": 0xFFFFFF,
    "AQUA": 0x1ABC9C,
    "GREEN": 0x2ECC71,
    "BLUE": 0x3498DB,
    "PURPLE": 0x9B59B6,
    "LUMINOUS_VIVID_PINK": 0xE91E63,
    "GOLD": 0xF1C40F,
    "ORANGE": 0xE67E22,
    "RED": 0xE74C3C,
    "NAVY": 0x34495E,
    "DARK_AQUA": 0x11806A,
    "DARK_GREEN": 0x1F8B4C,
    "DARK_BLUE": 0x206694,
    "DARK_PURPLE": 0x71368A,
    "DARK_VIVID_PINK": 0xAD1457,
    "DARK_GOLD": 0xC27C0E,
    "DARK_ORANGE": 0xA84300,
    "DARK_RED": 0x992D22,
    "DARK_NAVY": 0x2C3E50,
}

client.color_list = [c for c in client.colors.values()]

# EVENTS
@client.event
async def on_ready():
    
    # On ready, print some details to standard out
    print(
        f"-----\nLogged in as: {client.user.name} : {client.user.id}\n-----\nMy current prefix is: t!\n-----"
    )    


    # Adding MongoDB to our bot
    client.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(client.connection_url))
    client.db = client.mongo["pythonbot"]
    client.config = Document(client.db, "config")   
    print("Initialized Database\n-----")
    for document in await client.config.get_all():
        print(document)
  
        
    for cog in client.cogs:
        print(f"Loaded {cog} \n-----")    

@client.event
async def on_message(message):
    # Ignore messages sent by yourself
    if message.author.bot:
        return

    # A way to blacklist users from the bot by not processing commands
    # if the author is in the blacklisted_users list
    if await Blacklist_DB(client).check_user_blacklisted_status(message.author.id):
        embed = nextcord.Embed(title="🚫 Sorry! You are not allowed to use my command.", color=0x00FFFF)
        msg = await message.author.send(embed=embed)
        return None
    
    # Whenever the bot is tagged, respond with its prefix
    if message.content.startswith(f"<@!{client.user.id}>") and \
        len(message.content) == len(f"<@!{client.user.id}>"
    ):
        data = await client.config.find(message.guild.id)
        prefix = data.get("prefix", "t!")
        await message.channel.send(f"My prefix here is `{prefix}`", delete_after=20)

    await client.process_commands(message)


 

# Error Handling
@client.event
async def on_command_error(ctx, error):
    view = DelBtn(ctx)
  
    errorEmbed = nextcord.Embed(
        title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
    errorEmbed.set_author(
        name="OpenSourceGames Utility", icon_url=client.user.display_avatar)
    
    if isinstance(error, commands.errors.MissingRequiredArgument):
        errorEmbed.add_field(
        name="Error is described below.", value=f"**Type:** {type(error)}\n\n```You're missing a required argument.```") 
    else:    
       errorEmbed.add_field(
        name="Error is described below.", value=f"**Type:** {type(error)}\n\n```py\n {error}\n```")
    errorEmbed.add_field(
        name="__**What To do?**__", value="Don't worry we will forward this message to the devs.\n\n**Read the faqs for common errors at:** [click here](https://opensourcegames.gitbook.io/nextcord-bot-template/faqs)", inline=False)
    errorEmbed.set_footer(
        text=f"Command requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
   
    await ctx.send(embed=errorEmbed, view=view)
    
@client.event
async def on_application_command_error(interaction, error):
    view = DelBtnSlashInteractionCheck(interaction)
  
    errorEmbed = nextcord.Embed(
        title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
    errorEmbed.set_author(
        name="OpenSourceGames Utility", icon_url=interaction.client.user.display_avatar)
    
    if isinstance(error, commands.errors.MissingRequiredArgument):
        errorEmbed.add_field(
        name="Error is described below.", value=f"**Type:** {type(error)}\n\n```You're missing a required argument.```") 
    else:    
       errorEmbed.add_field(
        name="Error is described below.", value=f"**Type:** {type(error)}\n\n```py\n {error}\n```")
       
    errorEmbed.add_field(
        name="__**What To do?**__", value="Don't worry we will forward this message to the dev.\n\n**Read the faqs for common errors at:** [click here](https://opensourcegames.gitbook.io/nextcord-bot-template/faqs)", inline=False)
    errorEmbed.set_footer(
        text=f"Command requested by {interaction.user.name}", icon_url=interaction.user.display_avatar)
   
    await interaction.response.send_message(embed=errorEmbed, ephemeral=True)


# RUNNING OUR CLIENT
if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this

    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("__"):
            client.load_extension(f"cogs.{file[:-3]}")
             
           

    client.run(client.config_token)
