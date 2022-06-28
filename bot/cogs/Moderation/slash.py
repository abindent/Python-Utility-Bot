import nextcord
from nextcord.ext import commands, application_checks


from util.constants import Client

class ModerationSlash(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="kick", description="Kicks the mentioned member from the server.") 
    @application_checks.has_guild_permissions(kick_members=True)
    async def kick_slash(self, interaction: nextcord.Interaction,  member: nextcord.Member = nextcord.SlashOption(name="member", description="Mention the Memebr."), reason: str = nextcord.SlashOption(name="reason", description="Why do you want to kick that memebr?")):    
        kickembed = nextcord.Embed(
            title=f"🔨 Kicked {member.name}", description=f"**The {member.name} has been kicked from the server due to the following reason:**\n**{reason}**")
        kickembed.set_author(
            name=Client.name, icon_url=self.bot.user.display_avatar)
        kickembed.set_footer(
            text=f"Command requested by {interaction.user.name}")
        await interaction.guild.kick(user=member, reason=reason)
        await interaction.response.send_message(embed=kickembed, ephemeral=True)

    @nextcord.slash_command(name="ban", description="Bans the mentioned member from the server.") 
    @application_checks.has_guild_permissions(ban_members=True)
    async def ban_slash(self, interaction: nextcord.Interaction,  member: nextcord.Member = nextcord.SlashOption(name="member", description="Mention the Memebr."), reason: str = nextcord.SlashOption(name="reason", description="Why do you want to ban that memebr?")):    
        banembed = nextcord.Embed(
            title=f"🔨 Banned {member.name}", description=f"**The {member.name} has been banned from the server due to the following reason:**\n**{reason}**")
        banembed.set_author(
            name=Client.name, icon_url=self.bot.user.display_avatar)
        banembed.set_footer(
            text=f"Command requested by {interaction.user.name}")
        await interaction.guild.ban(user=member, reason=reason)
        await interaction.response.send_message(embed=banembed, ephemeral=True)