import os
import dotenv
import datetime
import platform
import nextcord
import quickchart
from nextcord.ext import commands, menus
from utils.vote_utils import VoteManage

dotenv.load_dotenv()


class VoteButtonMenu(menus.ButtonMenu):
    def __init__(self, bot):
        super().__init__(disable_buttons_after=True)
        self.voteManage = VoteManage(bot)
        self.__id = os.getenv("secret_id")

    def makechart(self, likes, dislikes):
        qc = quickchart.QuickChart()
        qc.width = 640
        qc.height = 480
        qc.background_color = "#0D0C1D"
        qc.config = {
            "type": "outlabeledPie",
            "data": {
                "labels": ["Likes", "Dislikes"],
                "datasets": [{
                    "backgroundColor": ["#00FF00", "#FF0000"],
                    "data": [likes, dislikes],
                    "borderColor":'#00000000'
                }]
            },
            "options": {

                "title": {
                    "text": 'Vote Results',
                    "display": True,
                    "fontColor": 'white',
                    "fontSize": 20,
                    "fontFamily": 'lato'
                },
                "legend": {
                    "position": 'right',
                    "labels" : {
                        "fontColor" : "white"
                    }
                },
                'plugins': {
                    "outlabels": {
                        "text": "%l %p",
                        "color": "white",
                        "stretch": 30,
                        "font": {
                           "minSize": 15,
                        }
                    }
                },
            }
        }

        url = qc.get_url()
        return url

    async def send_initial_message(self, ctx, channel):

        embed = nextcord.Embed(title="OpenSourceGames Utility ",
                               url="https://discord.io/OpenSourceGames", description="There is something about me.")
        embed.set_author(name="OpenSourceGames Utility ",
                         icon_url=self.bot.user.display_avatar)
        embed.add_field(
            name="About Me", value=f"I am {self.bot.user} who is serving your commands.", inline=True)
        embed.add_field(name="My Prefix",
                        value="My prefix is `t!`", inline=False)

        data = await self.voteManage.get_data(self.__id)

        likes = data["Likes"]
        dislikes = data["Dislikes"]

        url = self.makechart(likes, dislikes)

        embed.set_image(url=url)

        embed.add_field(
            name="Help", value="Visit [https://osourcegames.herokuapp.com/contact](https://osourcegames.herokuapp.com/contact)", inline=True)
        embed.set_footer(text="By OpenSourceGames Utility ▶️ About Me")

        # dict = {
        #     "_id": self.__id,
        #     "Likes" : 0,
        #     "Dislikes" : 0
        # }
        # await self.voteManage.create_vote(dict)

        return await channel.send(f'Hello {ctx.author.mention}', view=self, embed=embed)

    @nextcord.ui.button(emoji="\N{THUMBS UP SIGN}")
    async def on_thumbs_up(self, button, interaction: nextcord.Interaction):
        status = await self.voteManage.check_user_vote_status(interaction.user.id)
        if not status:
            dictionary = {
                "_id": interaction.user.id,
                "voted": True
            }

            await self.voteManage.add_user_data(dictionary)
            await self.voteManage.add_like(self.__id)

            embed = nextcord.Embed(title="OpenSourceGames Utility ",
                                   url="https://discord.io/OpenSourceGames", description="There is something about me.")
            embed.set_author(name="OpenSourceGames Utility ",
                             icon_url=self.bot.user.display_avatar)
            embed.add_field(
                name="About Me", value=f"I am {self.bot.user} who is serving your commands.", inline=True)
            embed.add_field(name="My Prefix",
                            value="My prefix is `t!`", inline=False)
            embed.add_field(name="Vote Status ",
                            value="Thanks for voting 👍", inline=False)
            embed.add_field(
                name="Help", value="Visit [https://osourcegames.herokuapp.com/contact](https://osourcegames.herokuapp.com/contact)", inline=True)
            embed.set_footer(text="By OpenSourceGames Utility ▶️ About Me")

            await self.message.edit(content=f"Thanks {interaction.user.mention} for voting 👍", embed=embed)

        else:
            await interaction.response.send_message(":no_entry: You have already voted for the bot!", ephemeral=True)

    @nextcord.ui.button(emoji="\N{THUMBS DOWN SIGN}")
    async def on_thumbs_down(self, button, interaction):
        status = await self.voteManage.check_user_vote_status(interaction.user.id)
        if not status:
            dictionary = {
                "_id": interaction.user.id,
                "voted": True
            }

            await self.voteManage.add_user_data(dictionary)
            await self.voteManage.add_dislike(self.__id)

            embed = nextcord.Embed(title="OpenSourceGames Utility ",
                                   url="https://discord.io/OpenSourceGames", description="There is something about me.")
            embed.set_author(name="OpenSourceGames Utility ",
                             icon_url=self.bot.user.display_avatar)
            embed.add_field(
                name="About Me", value=f"I am {self.bot.user} who is serving your commands.", inline=True)
            embed.add_field(name="My Prefix",
                            value="My prefix is `t!`", inline=False)
            embed.add_field(name="Vote Status ",
                            value="Thanks for voting 👎", inline=False)
            embed.add_field(
                name="Help", value="Visit [https://osourcegames.herokuapp.com/contact](https://osourcegames.herokuapp.com/contact)", inline=True)
            embed.set_footer(text="By OpenSourceGames Utility ▶️ About Me")
            await self.message.edit(content=f"Thanks {interaction.user.mention} for voting 👎", embed=embed)

        else:
            await interaction.response.send_message(":no_entry: You have already voted for the bot!", ephemeral=True)

    @nextcord.ui.button(emoji="<:dustbin:949602736633167882>")
    async def on_stop(self, button, interaction):
        await self.message.delete()


class DelBtn(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red, emoji="<:dustbin:949602736633167882>")
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()


class About(commands.Cog, name="Info about the Bot"):

    COG_EMOJI = "👷"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.command(name="vote", description="Vote me.")
    async def vote_bot(self, ctx):
        await VoteButtonMenu(self.bot).start(ctx)

    @commands.command(name="about", description="Shows some info about of the bot.", aliases=["botstats", "stats"])
    async def about(self, ctx):
        """
        A usefull command that displays bot statistics.
        """
        view = DelBtn()
        pythonVersion = platform.python_version()
        npyVersion = nextcord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        shard_id = ctx.guild.shard_id
        shard = self.bot.get_shard(shard_id)
        shard_ping = shard.latency
        shard_servers = len(
            [guild for guild in self.bot.guilds if guild.shard_id == shard_id])

        embed = nextcord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF',
                               colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value=self.bot.version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='nextcord.Py Version', value=npyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Shard ID:', value=shard_id)
        embed.add_field(name='Shard Ping:', value=shard_ping)
        embed.add_field(name='Shard Servers:', value=shard_servers)
        embed.add_field(name='Bot Developers:', value=self.bot.owner_id)

        embed.set_footer(
            text=f"{ctx.author.guild.name} | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.display_avatar)

        await ctx.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(About(bot))
