import asyncio
import nextcord
import random
import datetime
from nextcord.ext import commands, application_checks
from util.messages.buttons.suggestion import MakeStatusBtn, SuggestionBtn, MakeSuggesstionLink
from util.databases.suggestion import SuggestionDB


class Suggestion(commands.Cog, description="Give or control suggestions."):

    COG_EMOJI = "💡"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.db = SuggestionDB(self.bot)

    @commands.group(name="suggest", help="You member suggest us something.", usage="<suggestion>", invoke_without_command=True)
    async def suggest(self, ctx: commands.Context, *, suggestion):
        await ctx.message.delete()

        data = await self.db.get_data(ctx.guild.id)

        if not data:
            suggestion_channel = await ctx.guild.create_text_channel('📨｜suggestions')
            approve_channel = await ctx.guild.create_text_channel('✔｜approved-suggestions')
            deny_channel = await ctx.guild.create_text_channel('❌｜denied-suggestions')

            await self.db.add_data(ctx.guild.id, suggestion_channel.id, approve_channel.id, deny_channel.id)
            data = await self.db.get_data(ctx.guild.id)
            channel = self.bot.get_channel(data["channel_id"])
            count = data['suggestion_count']
            await self.db.add_suggestion_count(ctx.guild.id)

        else:
            data = await self.db.get_data(ctx.guild.id)
            channel = self.bot.get_channel(data["channel_id"])
            count = data['suggestion_count']
            await self.db.add_suggestion_count(ctx.guild.id)

        suggest = nextcord.Embed(title=f'Suggestion #{count}',
                                 description=f'{suggestion}', color=nextcord.Color.blue())
        suggest.set_author(
            name=ctx.author, icon_url=ctx.author.display_avatar)
        text = f"Author ID: {ctx.author.id}"
        suggest.set_footer(
            text=text)

        suggesting = await channel.send(embed=suggest, view=SuggestionBtn(self.db))
        await self.db.create_message_data(suggesting.id, ctx.author.id, count, suggestion)
        await ctx.author.send(f":) Suggestion ID: {suggesting.id}", view=MakeSuggesstionLink(ctx.message.guild.id, channel.id, suggesting.id))
        await suggesting.add_reaction("✅")
        await suggesting.add_reaction("❌")

    """ Making an approve command for suggesion command"""
    @suggest.command(name="approve", description="Approves a suggestion.", usage="<suggestion id> [reason]")
    @commands.has_guild_permissions(manage_messages=True, manage_channels=True)
    async def approve(self, ctx: commands.Context, id: int = None, *, reason="*No Reason is provided.*"):
        await ctx.message.delete()
        if id is None:
            return

        data = await self.db.get_data(ctx.guild.id)

        if not data:
            suggestion_channel = await ctx.guild.create_text_channel('📨｜suggestions')
            approve_channel = await ctx.guild.create_text_channel('✔｜approved-suggestions')
            deny_channel = await ctx.guild.create_text_channel('❌｜denied-suggestions')

            await self.db.add_data(ctx.guild.id, suggestion_channel.id, approve_channel.id, deny_channel.id)
            data = await self.db.get_data(ctx.guild.id)
            channel  = self.bot.get_channel(data["channel_id"])
            achannel = self.bot.get_channel(data["approve_channel_id"])
        
        channel  = self.bot.get_channel(data["channel_id"])
        achannel = self.bot.get_channel(data["approve_channel_id"])

         
        suggestionMsg = await channel.fetch_message(id)
        if not await self.db.check_approved(suggestionMsg.id):
            suggestion_data = await self.db.get_message_data(id)
            suggestion_message = suggestion_data["suggestion"]
            sno = suggestion_data["serial_no"]
            suggested_by = self.bot.get_user(suggestion_data["suggestor_id"])
          
            if suggestionMsg is None:
                msg = await ctx.send("Invalid suggestion ID provided.")
                await asyncio.sleep(3)
                await msg.delete()
        
            
            await self.db.update_review(id, isReviewed="accepted")
            
            embed = nextcord.Embed(
                title=f'✅ Suggestion #{sno} has been approved by {ctx.author}.', color=nextcord.Color.green())
            embed.set_author(
                name=f'{suggested_by.name}#{suggested_by.discriminator}', icon_url=suggested_by.display_avatar)
            embed.add_field(
                name="Suggestion", value=f'{suggestion_message}\n\n')
            embed.add_field(
                name="Reason", value=f"{reason}", inline=False)
            embed.set_footer(
                text=f"Auhtor ID: {suggestion_data['suggestor_id']}")
            
            await achannel.send(embed=embed, view=MakeSuggesstionLink(ctx.message.guild.id, channel.id, suggestionMsg.id))
            await suggestionMsg.edit(view=MakeStatusBtn("Approved", nextcord.ButtonStyle.green, "✅"))

        else:
            data = await self.db.get_message_data(id)
            msg = await ctx.send(f"Someone has already {data['isReviewed']} this suggestion.")
            await asyncio.sleep(3)
            await msg.delete()
    
    
    """ Making an deny command for suggesion command"""
    @suggest.command(name="deny", description="Declines a suggestion.", usage="<suggestion id> [reason]")
    @commands.has_guild_permissions(manage_messages=True, manage_channels=True)
    async def deny(self, ctx, id: int = None, *, reason="*No reason is provided.*"):
        await ctx.message.delete()
        if id is None:
            return

        data = await self.db.get_data(ctx.guild.id)

        if not data:
            suggestion_channel = await ctx.guild.create_text_channel('📨｜suggestions')
            approve_channel = await ctx.guild.create_text_channel('✔｜approved-suggestions')
            deny_channel = await ctx.guild.create_text_channel('❌｜denied-suggestions')

            await self.db.add_data(ctx.guild.id, suggestion_channel.id, approve_channel.id, deny_channel.id)
            data = await self.db.get_data(ctx.guild.id)
            channel  = self.bot.get_channel(data["channel_id"])
            dchannel = self.bot.get_channel(data["deny_channel_id"])

        channel  = self.bot.get_channel(data["channel_id"])
        dchannel = self.bot.get_channel(data["deny_channel_id"])
 
        suggestionMsg = await channel.fetch_message(id)
        if not await self.db.check_approved(suggestionMsg.id):
            suggestion_data = await self.db.get_message_data(id)
            suggestion_message = suggestion_data["suggestion"]
            sno = suggestion_data["serial_no"]
            suggested_by = self.bot.get_user(suggestion_data["suggestor_id"])

            if suggestionMsg is None:
                msg = await ctx.send("Invalid suggestion ID provided.")
                await asyncio.sleep(3)
                await msg.delete()

            
            await self.db.update_review(id, isReviewed="rejected")
            
            embed = nextcord.Embed(
                title=f'❌ Suggestion #{sno} has been rejected by {ctx.author}.', color=nextcord.Color.red())
            embed.set_author(
                name=f'{suggested_by.name}#{suggested_by.discriminator}', icon_url=suggested_by.display_avatar)
            embed.add_field(
                name="Suggestion", value=f'{suggestion_message}\n\n')
            embed.add_field(
                name="Reason", value=f"{reason}", inline=False)
            embed.set_footer(
                text=f"Auhtor ID: {suggestion_data['suggestor_id']}")
            
            await dchannel.send(embed=embed, view=MakeSuggesstionLink(ctx.message.guild.id, channel.id, suggestionMsg.id))
            await suggestionMsg.edit(view=MakeStatusBtn("Denied", nextcord.ButtonStyle.red, "❌"))
            
            await ctx.send("The default channel got deleted so set a channel. For more run `[prefix]help suggestion setup channel`")
          
  
        else:
            data = await self.db.get_message_data(id)
            msg = await ctx.send(f"Someone has already {data['isReviewed']} this suggestion.")
            await asyncio.sleep(3)
            await msg.delete()
 
        

    @commands.group(name="suggestion-setup", description=":gear: Sets up the suggestion system.", invoke_without_command=True)
    async def suggesion_set(self, ctx: commands.Context):
       await ctx.send("Please choose an option. For more use `[prefix]help suggestionset set`")

    @suggesion_set.group(name="channel", description="Sets channels for the suggestion system.", invoke_without_command=True)
    async def suggestion_set_channel(self, ctx: commands.Context):
       await ctx.send("Please choose an option. For more use `[prefix]help suggestionset set channel`")
    
    @suggestion_set_channel.command(name="suggestion", description="Sets the channel where the suggestions will be showed.")
    async def suggestion_channel_set(self, ctx: commands.Context, channel: nextcord.TextChannel):
        data = await self.db.get_data(ctx.guild.id)
        
        if data:
          await self.db.update_channel(ctx.guild.id, channel.id)
          msg = await ctx.send(f"Successfuly set {channel.mention} for showing suggestions.")
          await asyncio.sleep(3)
          await msg.delete()
          
        else:
            await self.db.add_data(ctx.guild.id, channel_id=channel.id) 
            msg = await ctx.send(f"Successfully set {channel.mention} for showing suggestions.") 
            await asyncio.sleep(3)
            await msg.delete()
  
    @suggestion_set_channel.command(name="approve", description="Sets the channel where the approved suggestions will be showed.")
    async def suggestion_approve_channel_set(self, ctx: commands.Context, channel: nextcord.TextChannel):
        data = await self.db.get_data(ctx.guild.id)
        
        if data:
         
          await self.db.update_approve_channel(ctx.guild.id, channel.id)
          msg = await ctx.send(f"Successfuly set {channel.mention} for showing approved suggestions.")
          await asyncio.sleep(3)
          await msg.delete()

        else:
            channel_id = data["channel_id"]                    
            deny_channel_id = data["deny_channel_id"]   
            await self.db.add_data(ctx.guild.id, channel_id=channel_id, approve_channel_id=channel.id, deny_channel_id=deny_channel_id) 
            msg = await ctx.send(f"Successfully set {channel.mention} for showing approved suggestions.") 
            await asyncio.sleep(3)
            await msg.delete()
            
    @suggestion_set_channel.command(name="deny", description="Sets the channel where the denied suggestions will be showed.")
    async def suggestion_deny_channel_set(self, ctx: commands.Context, channel: nextcord.TextChannel):
        data = await self.db.get_data(ctx.guild.id)
        
        if data:
          await self.db.update_deny_channel(ctx.guild.id, channel.id)
          msg = await ctx.send(f"Successfuly set {channel.mention} for showing denied suggestions.")
          await asyncio.sleep(3)
          await msg.delete()

        else:
            channel_id = data["channel_id"]                    
            approve_channel_id = data["approve_channel_id"]   
            await self.db.add_data(ctx.guild.id, channel_id=channel_id, approve_channel_id=approve_channel_id, deny_channel_id=channel.id) 
            msg = await ctx.send(f"Successfully set {channel.mention} for showing denied suggestions.") 
            await asyncio.sleep(3)
            await msg.delete()

