import nextcord
from nextcord.ext import commands, activities


class MakeLink(nextcord.ui.View):
    def __init__(self, link: str):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Join Game", url=f"{link}"))


class Activities(commands.Cog, name="Discord Activities"):

    COG_EMOJI = "🚀"

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, description="Creates activities in your serevr.")
    async def activity(self, ctx):
        return

    @activity.command(name="Skecth Heads", description="Creates `Skecth Heads crew` activity in your channel.")
    async def skecth_heads(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Please specify a channel to join/create the activity.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.sketch)

        except nextcord.HTTPException:
            msg = await ctx.send("Please mention a channel to join/create the activity.", delete_after=45)
            return msg

        embed = nextcord.Embed(
            title="Skecth Heads Crew Game", description=f"{ctx.author.mention} has created game in {channel.name}.", color=nextcord.Color.green())
        embed.add_field(
            name="What is it?", value="It's like skribble.io but in discord voice channel. Someone draws something and everyone else has to guess what is it.")
        embed.set_thumbnail(
            url="https://support.discord.com/hc/article_attachments/4503731144471/Discord_SketchHeads_Lobby.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))

    @activity.command(name="poker", description="Creates `poker` activity in your channel.")
    async def poker(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Please specify a channel to join/create the activity.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.poker)

        except nextcord.HTTPException:
            msg = await ctx.send("Please mention a channel to join/create the activity.", delete_after=45)
            return msg

        embed = nextcord.Embed(
            title="Poker Game", description=f"{ctx.author.mention} has created game in {channel.name}.", color=nextcord.Color.green())
        embed.add_field(name="What is it?", value="The Poker Night Activity is a Texas hold 'em style game we developed here at Discord. You can play with up to 8 players total per game (you + 7 others), and have up to 17 additional spectators max.")
        embed.set_thumbnail(
            url="https://support.discord.com/hc/article_attachments/1500015218941/Screen_Shot_2021-05-06_at_1.46.50_PM.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))

    @activity.command(name="chess", description="Creates `chess in the park` activity in your channel.")
    async def chess(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Please specify a channel to join/create the activity.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.chess)

        except nextcord.HTTPException:
            msg = await ctx.send("Please mention a channel to join/create the activity.", delete_after=45)
            return msg

        embed = nextcord.Embed(title="Chess in the park Game",
                               description=f"{ctx.author.mention} has created game in {channel.name}.", color=nextcord.Color.green())
        embed.add_field(
            name="What is it?", value="Chess in the Park is an Activity that have been developed here at Discord for playing chess with your friends!")
        embed.set_thumbnail(
            url="https://support.discord.com/hc/article_attachments/4404615637015/chess_banner.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))

    @activity.command(name="letter_league", description="Creates `letter_league` activity in your channel.")
    async def letter_league(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Please specify a channel to join/create the activity.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.letter_league)

        except nextcord.HTTPException:
            msg = await ctx.send("Please mention a channel to join/create the activity.", delete_after=45)
            return msg

        embed = nextcord.Embed(title="Letter League Game",
                               description=f"{ctx.author.mention} has created game in {channel.name}.", color=nextcord.Color.green())
        embed.add_field(name="What is it?",
                        value="Letter League is an Activity that have been developed here at Discord. Letter League is a game where you and your friends take turns placing letters on a shared game board to create words in a crossword-style. Spelling words with high earning letters and placing letters on special spaces earn players more points, so get your dictionaries and thesauri ready!")
        embed.set_thumbnail(
            url="https://support.discord.com/hc/article_attachments/4419631744535/LL_Lobby.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))

    @activity.command(name="checkers_in_the_park", description="Creates `checkers in the park in the park` activity in your channel.")
    async def checkers_in_the_park(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Please specify a channel to join/create the activity.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.checker)

        except nextcord.HTTPException:
            msg = await ctx.send("Please mention a channel to join/create the activity.", delete_after=45)
            return msg

        embed = nextcord.Embed(title="Checkers in the park Game",
                               description=f"{ctx.author.mention} has created game in {channel.name}.", color=nextcord.Color.green())
        embed.add_field(
            name="What is it?", value="Checkers in the Park is an Activity that have been developed here at Discord for playing checkers with your friends!")
        embed.set_thumbnail(
            url="https://support.discord.com/hc/article_attachments/4413878201879/checkers_splash.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))

    @activity.command(name="blazing_8s", description="Creates `Blazing 8s` activity in your channel.")
    async def blazing(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Please specify a channel to join/create the activity.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.blazing)

        except nextcord.HTTPException:
            msg = await ctx.send("Please mention a channel to join/create the activity.", delete_after=45)
            return msg

        embed = nextcord.Embed(title="Blazing 8s Game",
                               description=f"{ctx.author.mention} has created game in {channel.name}.", color=nextcord.Color.green())
        embed.add_field(name="What is it?", 
                        value=
             "Blazing 8s is an Activity that have been developed here at Discord. It is our Crazy Eights-inspired card game that you can play with your friends! The rules are simple — on your turn, discard a card from your hand with the same suit or number as the previous card. Playing special cards allows you to skip other players, reverse the direction of play, and even swap hands with other players."
             "The first person to discard all their cards wins!")
        embed.set_thumbnail(
            url="https://support.discord.com/hc/article_attachments/4487235506327/LoadingScreen.jpg")
        await ctx.send(embed=embed, view=MakeLink(invite_link))

    @activity.command(name="youtube", description="Creates `Youtube Watch Together` activity in your channel.")
    async def youtube(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Please specify a channel to join/create the activity.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.youtube)

        except nextcord.HTTPException:
            msg = await ctx.send("Please mention a channel to join/create the activity.", delete_after=45)
            return msg

        embed = nextcord.Embed(title="Youtube Watch Together",
                               description=f"{ctx.author.mention} has created game in {channel.name}.", color=nextcord.Color.green())
        embed.add_field(name="What is it?", 
                        value=
                        "It's an activity which lets you to run youtube inide discord vc.")
        embed.set_thumbnail(
            url="https://www.youtube.com/s/desktop/6007d895/img/favicon_32x32.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))

    @activity.command(name="word_snacks", description="Creates `Word Snacks` activity in your channel.")
    async def word_snacks(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Please specify a channel to join/create the activity.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.word_snacks)

        except nextcord.HTTPException:
            msg = await ctx.send("Please mention a channel to join/create the activity.", delete_after=45)
            return msg

        embed = nextcord.Embed(title="Word Snacks",
                               description=f"{ctx.author.mention} has created game in {channel.name}.", color=nextcord.Color.green())
        embed.add_field(name="What is it?", 
                        value=
                        "Word Snacks is an Activity that discord have developed in-house and is available on our official, public Discord Games Lab server. Word Snacks is a multiplayer word search game, where you and your friends try to make as many words as possible from a few letters. The more words you can spell before your opponents, the higher your score!")
        embed.set_thumbnail(
            url="https://support.discord.com/hc/article_attachments/4409234925463/word_snack_example.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))

    @activity.command(name="fishington", description="Creates `Fishington` activity in your channel.")
    async def fishington(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel is None:
            msg = await ctx.send("Please specify a channel to join/create the activity.", delete_after=45)
            return msg

        try:
            invite_link = await channel.create_activity_invite(activities.Activity.fishington)

        except nextcord.HTTPException:
            msg = await ctx.send("Please mention a channel to join/create the activity.", delete_after=45)
            return msg

        embed = nextcord.Embed(title="Fishington",
                               description=f"{ctx.author.mention} has created game in {channel.name}.", color=nextcord.Color.green())
        embed.add_field(name="What is it?", 
                        value=
                        "An online fishing game where you can relax, chat and fish with up to 24 players!")
        embed.set_thumbnail(
            url="https://betrayal.io/asset/image/share-card-fishington.png")
        await ctx.send(embed=embed, view=MakeLink(invite_link))


def setup(bot):
    bot.add_cog(Activities(bot))
