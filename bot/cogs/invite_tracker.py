import nextcord, NextcordUtils
from nextcord.ext import commands
from utils.mongo import Document

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
            embed.set_thumbnail(url=member.avatar.url)
            
            if member.guild.icon is not None:
             guild_url = member.guild.icon.url
            else:
                guild_url = "https://discord.com/assets/c09a43a372ba81e3018c3151d4ed4773.png"
                
            
            embed.set_footer(text=member.guild.name,
                            icon_url=guild_url)

            await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(InviteTracker(bot))
