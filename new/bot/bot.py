# IMPORTING THE PACKAGES
import os
import json
import logging
import datetime
import random
from pathlib import Path
from dotenv import load_dotenv
import motor.motor_asyncio
import discord
from discord.ext import commands


# LOADING EXTENSIONS FROM UTILS
from utils import json_loader
from utils.mongo import Document

# DATABASES
from utils.databases.blacklist import Blacklist_DB

# CONFIGURATIONS
cwd = str(Path(__file__).parents[0])

# LOADING ENVIRONMENT VARIABLES
load_dotenv()


class Client(commands.AutoShardedBot):

    def __init__(self, command_prefix, activity, intents, cwd):

        super().__init__(command_prefix=command_prefix, intents=intents)
       # BOT DETAILS
        self.version = "5.0.0"
        self.cwd = cwd
        self.guild_id = "932264473408966656"

        # DATABASE
        self.mongo = motor.motor_asyncio.AsyncIOMotorClient(
            str(os.getenv("MONGO_URI")))
        self.db = self.mongo["pythonbot"]
        self.config = Document(self.db, "config")

    async def on_ready(self):
        # On ready, print some details to standard out
        await self.load_extension("cogs.main")
            
        print(f"{self.cwd}\n-------")
        print(
            f"-----\nLogged in as: {self.user.name} : {self.user.id}\n-----\nMy default prefix is: t!\n-----"
        )
        for document in await self.config.get_all():
            print(document)
       

        for cog in self.cogs:
            print(f"Loaded {cog} \n-----")

    async def on_message(self, message: discord.Message):
        # Ignore messages sent by yourself
        if message.author.bot:
            return

        # A way to blacklist users from the bot by not processing commands
        # if the author is in the blacklisted_users list
        if await Blacklist_DB(self).check_user_blacklisted_status(message.author.id, message.guild.id):
            embed = discord.Embed(
                title="🚫 Sorry! You are not allowed to use my command.", color=0x00FFFF)
            msg = await message.author.send(embed=embed)
            return None

        if message.content.startswith(f"<@!{self.user.id}>") and \
            len(message.content) == len(f"<@!{self.user.id}>"
                                        ):
            data = await self.config.find(message.guild.id)
            prefix = data.get("prefix", "t!")
            await message.channel.send(f"My prefix here is `{prefix}`", delete_after=20)

        await self.process_commands(message)


# GETTING PREFIX FROM DATABASE
async def get_prefix(bot, message):
    if not message.guild:
        return commands.when_mentioned_or("t!")(bot, message)

    try:
        data = await bot.config.find(message.guild.id)

        # Make sure we have a useable prefix
        if not data or "prefix" not in data:
            return commands.when_mentioned_or("t!")(bot, message)
        return commands.when_mentioned_or(data["prefix"])(bot, message)
    except:
        return commands.when_mentioned_or("t!")(bot, message)

# INTENT
intent = discord.Intents.default()
intent.members = True
intent.message_content = True

# Changing Bot Presense
activity = discord.Game(name=f"Please interact with  me!")

# BOT
bot = Client(command_prefix=get_prefix,
             activity=activity, intents=intent, cwd=cwd)


# RUNNING OUR CLIENT
if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    
    bot.run(os.getenv("BOT_TOKEN"))
    
