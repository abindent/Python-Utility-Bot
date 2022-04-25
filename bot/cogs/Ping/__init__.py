import nextcord
from nextcord import Client
from nextcord.ext import commands

client = Client()
class Info(commands.Cog, description="Get the latency of the bot."):
    
    COG_EMOJI = "🏓"
    
    def __init__(self, bot):
        self.bot = bot
     
    @commands.command(name="ping", description="Returns the latency of the bot.", aliases=["latency", "p", "pingpong"])
    async def ping(self, ctx):
        await ctx.send(f"Pong! Latency is {self.bot.latency}ms")    


