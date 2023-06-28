import random, asyncio, nextcord
from nextcord.ext import commands
from utils.config_db import Blacklist_DB


class Configuration(commands.Cog):

    COG_EMOJI = "<:config:956526378008846437>"
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.blacklist_db = Blacklist_DB(self.bot)
   
          
   
    @commands.command(
        name="prefix",
        aliases=["changeprefix", "setprefix"],
        description="Change your guilds prefix!",
        usage="[prefix]",
    )
    @commands.cooldown(1, 2, commands.BucketType.member)
    @commands.has_guild_permissions(manage_guild=True)    
    async def prefix(self, ctx, *, prefix="t!"):
        await self.bot.config.upsert({"_id": ctx.guild.id, "prefix": prefix})
        await ctx.send(
            f"The guild prefix has been set to `{prefix}`. Use `{prefix}prefix [prefix]` to change it again!"
        )

    @commands.command(
        name="deleteprefix", aliases=["dp"], description="Delete your guilds prefix!"
    )
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def deleteprefix(self, ctx):
        await self.bot.config.unset({"_id": ctx.guild.id, "prefix": 1})
        await ctx.send("This guilds prefix has been set back to the default")



    """
    As a viewer, watch up to episode 10 and then attempt to convert the following
    to using a database rather then continuing to use json
    """

    @commands.command(
        name="blacklist", description="Blacklist a user from the bot", usage="<user>"
    )
    @commands.is_owner()
    async def blacklist(self, ctx: commands.Context, user: nextcord.Member):
        if ctx.message.author.id == user.id:
            msg = await ctx.send("🚫 Sorry! You cannot blacklist yourself!")
            await asyncio.sleep(5)
            await msg.delete()

        if await self.blacklist_db.check_user_blacklisted_status(user.id):
            embed = nextcord.Embed(title="🚫 Sorry! The user is already blacklisted", color=0x00FFFF)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
            
        else:
            await self.blacklist_db.create_user_table(ctx.message.guild.id, user)
            embed = nextcord.Embed(title=f"✅ Successfully blacklisted {user.name}.", color=0x00FFFF)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
            

    @commands.command(
        name="unblacklist",
        description="Unblacklist a user from the bot",
        usage="<user>",
    )
    @commands.is_owner()
    async def unblacklist(self, ctx, user: nextcord.Member):
        """
        Unblacklist someone from the bot
        """
        if ctx.message.author.id == user.id:
            msg = await ctx.send("🚫 Sorry! You cannot unblacklist yourself!")
            await asyncio.sleep(5)
            await msg.delete()

        if not await self.blacklist_db.check_user_blacklisted_status(user.id):
            embed = nextcord.Embed(title="🚫 Sorry! The user is not blacklisted", color=0x00FFFF)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
            
        else:
            await self.blacklist_db.delete_user_table(user.id)
            embed = nextcord.Embed(title=f"✅ Successfully unblacklisted {user.name}.", color=0x00FFFF)
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
    
    @commands.command(
        name="logout",
        aliases=["close", "stopbot"],
        description="Log the bot out of nextcord!",
    )
    @commands.is_owner()
    async def logout(self, ctx):
        """
        If the user running the command owns the bot then this will disconnect the bot from nextcord.
        """
        await ctx.send(f"Hey {ctx.author.mention}, I am now logging out :wave:")
        await self.bot.close()



def setup(bot):
    bot.add_cog(Configuration(bot))
