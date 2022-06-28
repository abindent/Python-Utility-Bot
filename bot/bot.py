# IMPORTING THE PACKAGES
import os, json, nextcord, logging, datetime, random, time
from pathlib import Path
import motor.motor_asyncio
from nextcord.ext import commands

# LOADING EXTENSIONS FROM UTILS
from util.loaders import json
from util.mongo import Document
from util.constants import Client, Database, Tokens
from util.databases import config
from util.messages import DeleteMessage



# CONFIGURATIONS
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-------")


# GETTING PREFIX FROM DATABASE
async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or(Client.default_prefix)(bot, message)

    try:
        data = await client.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or(Client.default_prefix)(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or(Client.default_prefix)(bot, message)


# Changing Bot Presense
activity = nextcord.Game(name=f"Please interact with  me!")

# Intents
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
    
# OUR CLIENT     
client = commands.AutoShardedBot(command_prefix=get_prefix, case_insensitive=True, activity=activity, intents=intents)


client.bot_version = Client.bot_version
client.guild_id= Client.guild_id
logging.basicConfig(level=logging.INFO)



# EVENTS
@client.event
async def on_ready():
    
    # Adding the start time
    client.start_time = time.time()

    # On ready, print some details to standard out
    print(
        f"-----\nLogged in as: {client.user.name} : {client.user.id}\n-----\nMy current prefix is: t!\n-----"
    )    


    # Adding MongoDB to our bot
    client.db = Database.db
    client.config = Document(client.db, "config")   
    print("Initialized Database\n-----")
    for document in await client.config.get_all():
        print(f'{document}\n-----')

 
        
    for cog in client.cogs:
        print(f"Loaded {cog} \n-----")  


@client.event
async def on_message(message):
    # Ignore messages sent by yourself
    if message.author.bot:
        return

    # A way to blacklist users from the bot by not processing commands
    # if the author is in the blacklisted_users list
    if await config.Blacklist_DB(client).check_user_blacklisted_status(message.author.id):
        embed = nextcord.Embed(title="🚫 Sorry! You are not allowed to use my command.", color=0x00FFFF)
        msg = await message.author.send(embed=embed)
        return None
    
    # Whenever the bot is tagged, respond with its prefix
    if message.content.startswith(f"<@{client.user.id}>") and len(message.content) == len(f"<@{client.user.id}>"):
        data = await client.config.find(message.guild.id)
        prefix = data.get("prefix", "t!")
        await message.channel.send(f"My prefix here is `{prefix}`", delete_after=20)

    await client.process_commands(message)


# Error Handling
@client.event
async def on_command_error(ctx, error):
    view = DeleteMessage(ctx)
  
    errorEmbed = nextcord.Embed(
        title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
    errorEmbed.set_author(
        name="OpenSourceGames Utility", icon_url=client.user.display_avatar)
    
    if isinstance(error, commands.errors.MissingRequiredArgument):
        errorEmbed.add_field(
        name="Error is described below.", value=f"**Type:** {type(error)}\n\n```You're missing a required argument.```") 
    else:    
       errorEmbed.add_field(
        name="Error is described below.", value=f"**Type:** {type(error)}\n\n```py\n{error}\n```")
    errorEmbed.add_field(
        name="__**What To do?**__", value="Don't worry we will forward this message to the devs.\n\n**Read the faqs for common errors at:** [click here](https://opensourcegames.gitbook.io/nextcord-bot-template/faqs)", inline=False)
    errorEmbed.set_footer(
        text=f"Command requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
   
    await ctx.send(embed=errorEmbed, view=view)
    
@client.event
async def on_application_command_error(interaction, error):
  
    errorEmbed = nextcord.Embed(
        title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
    errorEmbed.set_author(
        name="OpenSourceGames Utility", icon_url=interaction.client.user.display_avatar)
    
    if isinstance(error, commands.errors.MissingRequiredArgument):
        errorEmbed.add_field(
        name="Error is described below.", value=f"**Type:** {type(error)}\n\n```You're missing a required argument.```") 
    else:    
       errorEmbed.add_field(
        name="Error is described below.", value=f"**Type:** {type(error)}\n\n```py\n{error}\n```")
       
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
        if file.endswith(".py") and not file.startswith("__pycache"):
            client.load_extension(f"cogs.{file[:-3]}")



           

    client.run(Client.token)


           

