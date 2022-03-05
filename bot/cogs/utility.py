import asyncio 
import datetime
import nextcord
import humanfriendly
import nextcord
from nextcord.ext import commands


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")  

    @commands.command(name="clear",description="Clears messages",pass_context=True)
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, amount: int):        
      if amount > 1000 :
          message = await ctx.send('Cannot delete more than 500 messages.')
          await asyncio.sleep(5)
          await message.delete()
      else:
          new_count = {}
          messages = await ctx.channel.history(limit=amount).flatten()
          for message in messages:
              if str(message.author) in new_count:
                  new_count[str(message.author)] += 1
              else:
                  new_count[str(message.author)] = 1
          deleted_messages = 0  
          new_string = []
          for author, message_deleted in list(new_count.items()):                
                new_string.append(f"**{author}**: {message_deleted}")
                deleted_messages += message_deleted    
          new_message = '\n'.join(new_string)  
          await ctx.channel.purge(limit=amount+1)
          message = await ctx.send(f"Successfully cleared `{deleted_messages} messages`\n\n{new_message}")
          await asyncio.sleep(3)
          await message.delete()

    @commands.command(name="toggle", aliases=["togglecmd", "editcmd"], description="Enables a Disabled Command and Disables an Enabled Command.")
    @commands.has_guild_permissions(administrator=True)
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)

        if command == None:
            await ctx.send(f"**Requested command 😞 {command.name} not found.**")
        elif ctx.command == command:
            await ctx.send(f"{command.name} cannot be disabled.")
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            togglembed = nextcord.Embed(
                title=f"Toggled {command.qualified_name}", description=f"**The {command.qualified_name} command has been {ternary}**")
            togglembed.set_author(
            name="Utility Bot", icon_url=self.bot.user.display_avatar)
            togglembed.set_footer(
                text=f"Command requested by {ctx.author.name}")
            await ctx.send(embed=togglembed)

    
    @commands.command(name="ban", aliases=["modbancmd"], description="Bans the mentioned user.")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: nextcord.Member, *, reason=None):
        banembed = nextcord.Embed(
            title=f"🔨 Banned {member.name}", description=f"**The {member.name} has been banned from the server due to the following reason:**\n**{reason}**")
        banembed.set_author(
            name="Utility Bot", icon_url=self.bot.user.display_avatar)
        banembed.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await member.ban(reason=reason)
        await ctx.send(embed=banembed)

    @commands.command(name="unban", aliases=["modunban", "removeban"], description="Unbans the mentioned user.")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                unbanembed = nextcord.Embed(
                    title=f"🔨 Unbanned {user.name}", description=f"**The {user.name}#{user.discriminator} has been unbanned from the server .**")
                unbanembed.set_author(
            name="Utility Bot", icon_url=self.bot.user.display_avatar)
                unbanembed.set_footer(
                    text=f"Command requested by {ctx.author.name}")
                await ctx.send(embed=unbanembed)
                return
    @commands.command(name="kick", aliases=["modkickcmd"], description="Kicks the mentioned user.")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: nextcord.Member, *, reason=None):
        kickembed = nextcord.Embed(
            title=f"🔨 Kicked {member.name}", description=f"**The {member.name} has been kicked from the server due to the following reason:**\n**{reason}**")
        kickembed.set_author(
            name="Utility Bot", icon_url=self.bot.user.display_avatar)
        kickembed.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await member.kick(reason=reason)
        await ctx.send(embed=kickembed)

    @commands.command(name="mute", aliases=["modmutecmd"], description="Mutes the mentioned user.")
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: nextcord.Member, time, *, reason):
        muteembed = nextcord.Embed(
            title=f"🔨 Muted {member.name}", description=f"**The {member.name} has been muted due to the following reason:**\n**{reason}**")
        muteembed.set_author(
            name="Utility Bot", icon_url=self.bot.user.display_avatar)
        muteembed.set_footer(
            text=f"Command requested by {ctx.author.name}")
        time = humanfriendly.parse_timespan(time)
        await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time), reason=reason)
        await ctx.send(embed=muteembed)        

    @commands.command(name="unmute", aliases=["modunmutecmd"], description="Unmutes the mentioned user.")
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: nextcord.Member, *, reason):
        unmuteembed = nextcord.Embed(
            title=f"🔨 Unmuted {member.name}", description=f"**The {member.name} has been unmuted due to the following reason:**\n**{reason}**")
        unmuteembed.set_author(
            name="Utility Bot", icon_url=self.bot.user.display_avatar)
        unmuteembed.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await member.edit(timeout=None, reason=reason)
        await ctx.send(embed=unmuteembed)    

 
def setup(bot):
    bot.add_cog(Utility(bot))
