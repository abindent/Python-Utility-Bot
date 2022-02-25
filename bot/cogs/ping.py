import nextcord
from nextcord import Client
from nextcord.ext import commands

client = Client()
class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")
        
    @commands.command(name="ping", description="Returns the latency of the bot", aliases=["latency", "p", "pingpong"])
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency is {round(self.bot.latency)}ws")    


def setup(bot):
    bot.add_cog(Info(bot))