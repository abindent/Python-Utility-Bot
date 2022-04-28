import nextcord
from nextcord.ext import commands

class CogSetup(commands.Cog, name="Extension Setup", description="Load, Unload or Reload the extensions."):
     def __init__(self, bot):
        self.bot = bot
     
     COG_EMOJI = "⚙️"

    
    # Load Command
     @commands.command(name="load", description="Load the cogs.", usage="<cog_name or extension_name>")
     @commands.is_owner()
     async def load(self, ctx, extensions):
        self.bot.load_extension(f"cogs.{extensions}") 
        await ctx.send("Loaded Cogs")

    # Unload Comamnd
     @commands.command(name="unload", description="Unload the cogs.", usage="<cog_name or extension_name>")
     @commands.is_owner()
     async def unload(self, ctx, extensions):
        self.bot.unload_extension(f"cogs.{extensions}")
        await ctx.send("Unloaded Cogs")

    # Reload Command
     @commands.command(name="reload", description="Reload the cogs.", usage="<cog_name or extension_name>")
     @commands.is_owner()
     async def reload(self, ctx, extensions):
        self.bot.reload_extension(f"cogs.{extensions}")
        await ctx.send("Reloaded Cogs")

    
