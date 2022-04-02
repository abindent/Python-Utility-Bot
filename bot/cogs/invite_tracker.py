import nextcord, NextcordUtils
from nextcord.ext import commands
from utils.mongo import Document
from bot import DelBtn

class InviteDB:
    def __init__(self, bot):
       self.invites = Document(bot.db, "invites") 

class InviteTracker(commands.Cog, name="Tracker for the bot."):

    COG_EMOJI = "🏥"

    def __init__(self, bot):
        self.bot = bot
        self.tracker = NextcordUtils.InviteTracker(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.tracker.cache_invites()
        self.invites = InviteDB(self.bot).invites

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        await self.tracker.update_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.tracker.add_guild_cache(guild)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        await self.tracker.remove_invite_cache(invite)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.tracker.remove_guild_cache(guild)

    @commands.Cog.listener()
    async def on_member_join(self, member: nextcord.Member):
        try:  
            inviter = await self.tracker.fetch_inviter(member)
            data = await self.invites.find_by_custom(
                {"guild_id": member.guild.id, "inviter_id": inviter.id}
            )
            if data is None:
                data = {
                    "guild_id": member.guild.id,
                    "inviter_id": inviter.id,
                    "count": 0,
                    "invited_users": []
                }

            data["count"] += 1
            data["invited_users"].append(member.id)
            await self.invites.upsert_custom(
                {"guild_id": member.guild.id, "inviter_id": inviter.id}, data
            )

            channel = nextcord.utils.get(member.guild.channels, name="invite-logs")
        
            if channel is None:
                await member.guild.create_text_channel("invite-logs")
                channel = nextcord.utils.get(member.guild.channels, name="invite-logs")
              
            
            embed = nextcord.Embed(
                title=f"Welcome {member.name}", description=f"Invited by: {inviter.mention}\nInvites: {data['count']}", timestamp=member.joined_at)
            embed.set_thumbnail(url=member.display_avatar)
            embed.set_footer(text=memebr.guild.name,
                            icon_url=member.guild.icon.url)

            await channel.send(embed=embed, view=DelBtn())
        
        except Exception as error:
            print(error)

def setup(bot):
    bot.add_cog(InviteTracker(bot))
