import nextcord
from nextcord.ext import commands

# See channels.py for this being used on the bot


class Groups(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

""" The commmand group below is a group of commands having sub-commands.We often use [prefix][main_command] [subcommand(always optional)] [url] this type of things in bots.
For maintainance and a lot of issues we usually split the funtionality of the parent command into different child subcommands.You can use or not but you can split them."""
        
    @commands.group(invoke_without_command=True)
    async def first(self, ctx):
        """ This code will be excecuted when running this parent command. """
        await ctx.send("This is the first command layer")

    @first.group(invoke_without_command=True)
    async def second(self, ctx, channel: nextcord.TextChannel=None):
         """ This code will be excecuted when using this child subcommand with parent command. """
            
        # Getiing the channel id if  provided 
        if channel_id not None:
     
            # Sending the message to the mentioned channel
            await channel.send(
                "Hey! This is a message from me the bot. Bet you didn't see who ran the command?",
                delete_after=15,
            )

    @second.command()
    async def third(self, ctx, channelId=None):
         """ This code will be excecuted when using this child subcommand with the parent command. """
         # Sending a message to the author
        await ctx.message.author.send("Hey! Did this come through clearly?")


def setup(bot):
    bot.add_cog(Groups(bot))
