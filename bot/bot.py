# IMPORTING THE PACKAGES
import os, json, nextcord, logging, datetime, random
from pathlib import Path
import motor.motor_asyncio
from nextcord.ext import commands
from dotenv import load_dotenv

# LOADING EXTENSIONS FROM UTILS
from utils import json_loader
from utils.mongo import Document

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

# OUR CLIENT 
client = commands.AutoShardedClient(command_prefix=get_prefix, case_insensitive=True)
client.config_token = os.getenv("BOT_TOKEN")
client.connection_url = os.getenv("MONGO_URI")
client.guild_id="932264473408966656"
logging.basicConfig(level=logging.INFO)

client.blacklisted_users = []
client.cwd = cwd

client.version = "10"

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
    # Changing Bot Presense
    await client.change_presence(
        activity=nextcord.Game(name=f"Hi I am {client.user.name}.\nPlease interact with me!")
    )

    # Adding MongoDB to our bot
    client.mongo = motor.motor_asyncio.AsyncIOMotorClient(str(client.connection_url))
    client.db = client.mongo["pythonbot"]
    client.config = Document(client.db, "config")
    print("Initialized Database\n-----")
    for document in await client.config.get_all():
        print(document)

@client.event
async def on_message(message):
    # Ignore messages sent by yourself
    if message.author.bot:
        return

    # A way to blacklist users from the bot by not processing commands
    # if the author is in the blacklisted_users list
    if message.author.id in client.blacklisted_users:
        return

    # Whenever the bot is tagged, respond with its prefix
    if message.content.startswith(f"<@!{client.user.id}>") and \
        len(message.content) == len(f"<@!{client.user.id}>"
    ):
        data = await client.config.get_by_id(message.guild.id)
        if not data or "prefix" not in data:
            prefix = "t!"
        else:
            prefix = data["prefix"]
        await message.channel.send(f"My prefix here is `{prefix}`", delete_after=15)

    await client.process_commands(message)

# Lang command
# DropDown View
# SELECT MENUS AND BUTTONS
class DropDown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(label="Python", description="Python is a user friendly language born from C language."),
            nextcord.SelectOption(label="JavaScript", description="JavaScript is a very popular language can be executed by the browser."),\
            nextcord.SelectOption(label="HTML", description="HTML is mandatory while building websites."),
            nextcord.SelectOption(label="CSS", description="Raw HTML looks bad, so CSS styles and decorates it."),
            nextcord.SelectOption(label="PHP", description="PHP is also a very popular language (used in Wordpress).")
        ]
        super().__init__(placeholder="Select Your Language", min_values=1, max_values=1, options=options)
    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Python":
             langembed = nextcord.Embed(
               title=f":wave: Hi {interaction.user.name}", description="**You have choosed <:python:935932879714779227> python.**")
           
             langembed.set_author(
        name="TechTon Bot", icon_url=client.user.display_avatar, url="https://python.org")   
             langembed.add_field(name="__ABOUT__", value="***Python is an interpreted high-level general-purpose programming language. Its design philosophy emphasizes code readability with its use of significant indentation. Its language constructs as well as its object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects***") 
            
             await interaction.response.edit_message(embed=langembed)
                
        if self.values[0] == "JavaScript":
             langembed = nextcord.Embed(
               title=f":wave: Hi {interaction.user.name}", description="**You have choosed <:JS:935933057800757318> javascript.**")
 
             langembed.set_author(
        name="TechTon Bot", icon_url=client.user.display_avatar, url="https://javascript.com")   
             langembed.add_field(name="__ABOUT__", value="***JavaScript, often abbreviated JS, is a programming language that is one of the core technologies of the World Wide Web, alongside HTML and CSS. Over 97% of websites use JavaScript on the client side for web page behavior, often incorporating third-party libraries.***") 
             await interaction.response.edit_message(embed=langembed)    
            
        if self.values[0] == "HTML":
             langembed = nextcord.Embed(
               title=f":wave: Hi {interaction.user.name}", description="**You have choosed <:html:935933258439483442> HTML.**")
 
             langembed.set_author(
        name="TechTon Bot", icon_url=client.user.display_avatar, url="https://html.com")   
             langembed.add_field(name="__ABOUT__", value="***The HyperText Markup Language, or HTML is the standard markup language for documents designed to be displayed in a web browser. It can be assisted by technologies such as Cascading Style Sheets (CSS) and scripting languages such as JavaScript. ... HTML elements are the building blocks of HTML pages.***") 
             await interaction.response.edit_message(embed=langembed) 
        if self.values[0] == "CSS":
             langembed = nextcord.Embed(
               title=f":wave: Hi {interaction.user.name}", description="**You have choosed <:css:935935867468533830> CSS.**")
 
             langembed.set_author(
        name="TechTon Bot", icon_url=client.user.display_avatar, url="https://g.co/kgs/83EKjE")   
             langembed.add_field(name="__ABOUT__", value="***Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML. CSS is a cornerstone technology of the World Wide Web, alongside HTML and JavaScripts.***") 
             await interaction.response.edit_message(embed=langembed) 
        if self.values[0] == "PHP":
             langembed = nextcord.Embed(
               title=f":wave: Hi {interaction.user.name}", description="**You have choosed <:php:935937346799546408> PHP.**")
 
             langembed.set_author(
        name="TechTon Bot", icon_url=client.user.display_avatar, url="https://php.net/")   
             langembed.add_field(name="__ABOUT__", value="***PHP is a general-purpose scripting language geared towards web development. It was originally created by Danish-Canadian programmer Rasmus Lerdorf in 1994. The PHP reference implementation is now produced by The PHP Group.***") 
             await interaction.response.edit_message(embed=langembed) 

class DropDownView(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(DropDown())
@client.command(name="lang", description="Choose your language and learn about it.")
async def _lang(ctx):
    view = DropDownView()
    langembed = nextcord.Embed(
        title=f":wave: Hi User", description=f"**Please choose your language from the opion below.**")
    langembed.set_author(
        name="TechTon Bot", icon_url=client.user.display_avatar)
    langembed.set_footer(
        text=f"Command requested by {ctx.author.name}")
    await ctx.send(embed=langembed, view=view)
    
# SLASH COMMAND


# 8ball Slash Command
@client.slash_command(name="8ball", description="Let the 8 Ball Predict!\nthe future")
async def eightball(interaction: nextcord.Interaction, *, question):
    responses = [
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        "I'm feeling well",
        'Yes - definitely.',
        'You may rely on it.',
        'As I see it yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Better not tell you now.',
        'Concentrate and ask again.',
        "Don't count on it.",
        'I cannot predict now.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'VEry doubtfull.',
        'I am tired. *proceeds with sleeping*',
        'As I see it, yes.',
        'Yes.',
        'Positive',
        'From my point of view, yes',
        'Convinced.',
        'Most Likley.',
        'Chances High',
        'No.',
        'Negative.',
        'Not Convinced.',
        'Perhaps.',
        'Not Sure',
        'Mayby',
        'Im to lazy to predict.'
    ]
    await interaction.response.send_message(f":8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}", ephemeral=True)
    
# TOGGLE COMMANDS SLASH COMMAND
@client.slash_command(name="toggle", description="Enables a Disabled Command and Disables an Enabled Command.")
@commands.has_guild_permissions(administrator=True)
async def toggle(interaction: nextcord.Interaction, *, command):
    command = client.get_command(command)

    if command == None:
        await interaction.response.send_message(f"Requested command 😞 {command.name} not found.**", ephemeral=True)
    elif command == "toggle":
        await interaction.response.send_message(f"{command.name} cannot be disabled.", ephemeral=True)
    else:
        command.enabled = not command.enabled
        ternary = "enabled" if command.enabled else "disabled"
        togglembed = nextcord.Embed(
            title=f"Toggled {command.qualified_name}", description=f"**The {command.qualified_name} command has been {ternary}**")
        togglembed.set_author(
            name="TechTon Bot", icon_url=client.user.display_avatar)
        togglembed.set_footer(
            text=f"Command requested by {interaction.user.name}")
        await interaction.response.send_message(embed=togglembed, ephemeral=True)
# Lang Slash Command
@client.slash_command(name="lang", description="Choose your language and learn about it.")
async def _lang(interaction: nextcord.Interaction):
    view = DropDownView()
    langembed = nextcord.Embed(
        title=f":wave: Hi {interaction.user.name}", description=f"**Please choose your language from the opion below.**")
    langembed.set_author(
        name="TechTon Bot", icon_url=client.user.display_avatar)
    langembed.set_footer(
        text=f"Command requested by {interaction.user.name}")
    await interaction.response.send_message(embed=langembed, view=view, ephemeral=True)
    
# Clear Slash Command
@client.slash_command(name="clear",description="Clears messages")
@commands.has_permissions(administrator=True)
async def clear(interaction: nextcord.Interaction, limit: int):
        if limit > 500:
            await interaction.response.send_message('Cannot delete more than 500 messages.', ephemeral=True)
        else:
            await interaction.channel.purge(limit=limit) 
            await interaction.response.send_message(f'Cleared `{limit}` Messages', ephemeral=True) 
# Ping Slash Command
@client.slash_command(name="ping", description="Returns the latency of the bot")
async def ping(interaction: nextcord.Interaction):
    await interaction.response.send_message(f"Pong! Latency is {round(client.latency)}ms", ephemeral=True)          


# Error Handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url=client.user.display_avatar)
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.MissingRequiredArgument):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url=client.user.display_avatar)
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.MissingRole):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url=client.user.display_avatar)
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.MissingPermissions):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url=client.user.display_avatar)
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.CommandInvokeError):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url=client.user.display_avatar)
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.CommandOnCooldown):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url=client.user.display_avatar)
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.ConversionError):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url=client.user.display_avatar)
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.UserInputError):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url=client.user.display_avatar)
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.DisabledCommand):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url=client.user.display_avatar)
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)


# RUNNING OUR CLIENT
if __name__ == "__main__":
    # When running this file, if it is the 'main' file
    # I.E its not being imported from another python file run this
    for file in os.listdir(cwd + "/cogs"):
        if file.endswith(".py") and not file.startswith("_"):
            client.load_extension(f"cogs.{file[:-3]}")

    client.run(client.config_token)
