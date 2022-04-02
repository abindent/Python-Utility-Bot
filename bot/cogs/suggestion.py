import asyncio, nextcord, random
from nextcord.ext import commands



class Suggestion(commands.Cog):

    COG_EMOJI = "💡"
    
    def __init__(self, bot):
        self.bot = bot


 

    @commands.command(name="suggest", description="You member suggest us something.", usage="<suggestion>")
    async def suggest(self, ctx, *, suggestion):
        await ctx.message.delete()
        channel = nextcord.utils.get(ctx.guild.text_channels, name='📨｜suggestions')
        if channel is None:
            await ctx.guild.create_text_channel('📨｜suggestions')
            channel = nextcord.utils.get(
                ctx.guild.text_channels, name='📨｜suggestions')
        suggest = nextcord.Embed(title=f'📝 New Suggestion by {ctx.author.name} !',
                                description=f'**__{ctx.author.name} has suggested__**\n\n{suggestion}', color=0xf20c0c)
        suggest.set_author(
            name="OpenSourceGames Utility", icon_url=self.bot.user.display_avatar)
        suggest.set_footer(
            text=f"Command requested by {ctx.author.name} | 📝 BOT Kernel: 487#G7")
        suggesting = await channel.send(embed=suggest)
        await ctx.author.send(f"^^ Suggestion ID: {suggesting.id}")
        await suggesting.add_reaction("✅")
        await suggesting.add_reaction("❌")

    """ Making an approve command for suggesion command"""
    @commands.command(name="approve", description="Approves a suggestion.", usage="<suggestion id>")
    @commands.has_any_role('✴ ⊶▬▬⊶▬Staff▬⊷▬▬⊷ ✴', '⚙️Server Staff')
    async def approve(self, ctx, id: int = None):
        await ctx.message.delete()
        if id is None:
            return
        staff = nextcord.utils.get(ctx.guild.roles, name="⚙️Server Staff")
        if staff is None:
            staff = await ctx.guild.create_role(name="⚙️Server Staff", color=0x51f5e7)
            await ctx.send('Created Role `⚙️Server Staff`. Apply it to start controlling the suggestions.')

        channel = nextcord.utils.get(ctx.guild.text_channels, name="📨｜suggestions")
        if channel is None:
            return
        achannel = nextcord.utils.get(
            ctx.guild.text_channels, name="✔｜approved-suggestions")
        if achannel is None:
            achannel = await ctx.guild.create_text_channel('✔｜approved-suggestions')
            await ctx.send("Created `✔｜approved-suggestions` channel.Change the channel permission to get started.")
    
        suggestionMsg = await channel.fetch_message(id)
        embed = nextcord.Embed(title=f'Suggestion has been approved.',
                            description=f'The suggestion id of `{suggestionMsg.id}` has been approved by {ctx.author.name}', color=0xf20c0c)
        embed.set_author(
            name="OpenSourceGames Utility", icon_url=self.bot.user.display_avatar)
        embed.add_field(name="Link to the embed.",
                        value=f"[Click here ](https://discord.com/channels/{ctx.message.guild.id}/{channel.id}/{suggestionMsg.id}) to see the suggestion.")
        embed.set_footer(
            text=f"Command requested by {ctx.author.name} | 📝 BOT Kernel: 487#G7")
        await achannel.send(embed=embed)

    """ Making an deny command for suggesion command"""
    @commands.command(name="deny", description="Declines a suggestion.", usage="<suggestion id>")
    @commands.has_any_role('✴ ⊶▬▬⊶▬Staff▬⊷▬▬⊷ ✴', '⚙️Server Staff')
    async def deny(self, ctx, id: int = None):
        await ctx.message.delete()
        if id is None:
            return
        staff = nextcord.utils.get(ctx.guild.roles, name="⚙️Server Staff")
        if staff is None:
            staff = await ctx.guild.create_role(name="⚙️Server Staff", color=0x51f5e7)
            await ctx.send('Created Role `⚙️Server Staff`. Apply it to start controlling the suggestions.')
        channel = nextcord.utils.get(ctx.guild.text_channels, name="📨｜suggestions")
        if channel is None:
            return
        dchannel = nextcord.utils.get(
            ctx.guild.text_channels, name="❌｜denied-suggestions")
        if dchannel is None:
            dchannel = await ctx.guild.create_text_channel('❌｜denied-suggestions')
            await ctx.send("Created `❌｜denied-suggestions` channel.Change the channel permission to get started.")
    
        suggestionMsg = await channel.fetch_message(id)
        embed = nextcord.Embed(title=f'Suggestion has been denied.',
                            description=f'The suggestion id of `{suggestionMsg.id}` has been denied by {ctx.author.name}', color=0xf20c0c)
        embed.set_author(
            name="OpenSourceGames Utility", icon_url=self.bot.user.display_avatar)
        embed.add_field(name="Link to the embed.",
                        value=f"[Click here ](https://discord.com/channels/{ctx.message.guild.id}/{channel.id}/{suggestionMsg.id}) to see the suggestion.")
        embed.set_footer(
            text=f"Command requested by {ctx.author.name} | 📝 BOT Kernel: 487#G7")
        await dchannel.send(embed=embed)



def setup(bot):
    bot.add_cog(Suggestion(bot))
