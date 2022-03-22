import datetime, platform, json, nextcord
from nextcord.ext import commands, menus




class AboutButtonMenu(menus.ButtonMenu):
    def __init__(self):
        super().__init__(disable_buttons_after=True)

    async def send_initial_message(self, ctx, channel):
        embed=nextcord.Embed(title="OpenSourceGames Utility ", url="https://discord.io/OpenSourceGames", description="There is something about me.")
        embed.set_author(name="OpenSourceGames Utility ", icon_url=self.bot.user.display_avatar)
        embed.add_field(name="About Me", value=f"I am {self.bot.user} who is serving your commands.", inline=True)
        embed.add_field(name="My Prefix", value="My prefix is `t!`", inline=False)
        embed.add_field(name="Help", value="Visit [https://osourcegames.herokuapp.com/contact](https://osourcegames.herokuapp.com/contact)", inline=True)
        embed.set_footer(text="By OpenSourceGames Utility ▶️ About Me")

        return await channel.send(f'Hello {ctx.author.mention}', view=self, embed=embed)

    @nextcord.ui.button(emoji="\N{THUMBS UP SIGN}")
    async def on_thumbs_up(self, button, interaction):
        dictionary = {
            f"user-{interaction.user.id}-{datetime.datetime.utcnow()}" : f"{interaction.user.name}",
            f"vote_sign-{interaction.user.id}-{datetime.datetime.utcnow()}" : "👎",
            f"time-{interaction.user.id}-{datetime.datetime.utcnow()}": f"{datetime.datetime.utcnow()}"
        }
        with open(f"../bot/config/vote.json",'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            file_data.update(dictionary)
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file)

            
        embed=nextcord.Embed(title="OpenSourceGames Utility ", url="https://discord.io/OpenSourceGames", description="There is something about me.")
        embed.set_author(name="OpenSourceGames Utility ", icon_url=self.bot.user.display_avatar)
        embed.add_field(name="About Me", value=f"I am {self.bot.user} who is serving your commands.", inline=True)
        embed.add_field(name="My Prefix", value="My prefix is `t!`", inline=False)
        embed.add_field(name="Status ", value="Thanks for voting 👍", inline=False)
        embed.add_field(name="Help", value="Visit [https://osourcegames.herokuapp.com/contact](https://osourcegames.herokuapp.com/contact)", inline=True)
        embed.set_footer(text="By OpenSourceGames Utility ▶️ About Me")
        

        await self.message.edit(content=f"Thanks {interaction.user.mention} for voting 👍",embed=embed)


    @nextcord.ui.button(emoji="\N{THUMBS DOWN SIGN}")
    async def on_thumbs_down(self, button, interaction):
        dictionary = {
            f"user-{interaction.user.name}" : f"{interaction.user.name}",
            f"current_vote-{interaction.user.name}" : "👎",
            f"time-{interaction.user.name}": f"{datetime.datetime.utcnow()}"
        }
        with open(f"../bot/config/vote.json", 'r+') as file:
            # First we load existing data into a dict.
            file_data = json.load(file)
            # Join new_data with file_data inside emp_details
            file_data.update(dictionary)
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file)
            
        embed=nextcord.Embed(title="OpenSourceGames Utility ", url="https://discord.io/OpenSourceGames", description="There is something about me.")
        embed.set_author(name="OpenSourceGames Utility ", icon_url=self.bot.user.display_avatar)
        embed.add_field(name="About Me", value=f"I am {self.bot.user} who is serving your commands.", inline=True)
        embed.add_field(name="My Prefix", value="My prefix is `t!`", inline=False)
        embed.add_field(name="Status ", value="Thanks for voting 👎", inline=False)
        embed.add_field(name="Help", value="Visit [https://osourcegames.herokuapp.com/contact](https://osourcegames.herokuapp.com/contact)", inline=True)
        embed.set_footer(text="By OpenSourceGames Utility ▶️ About Me")
        await self.message.edit(content=f"Thanks {interaction.user.mention} for voting 👎",embed=embed)

    @nextcord.ui.button(emoji="<:dustbin:949602736633167882>")
    async def on_stop(self, button, interaction):
        await self.message.delete()

class DelBtn(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.red, emoji="<:dustbin:949602736633167882>")  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()
 
class About(commands.Cog, name="Info about the Bot",):

    COG_EMOJI = "👷"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")  

    @commands.command(name="about", description="About me.")  
    async def button_menu_example(self, ctx):
        await AboutButtonMenu().start(ctx)    

    @commands.command(name="stats", description="Shows the stats of the bot.",aliases=["botstats"])
    async def stats(self, ctx):
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
        shard_servers = len([guild for guild in self.bot.guilds if guild.shard_id == shard_id])

        embed = nextcord.Embed(title=f'{self.bot.user.name} Stats', description='\uFEFF', colour=ctx.author.colour, timestamp=ctx.message.created_at)

        embed.add_field(name='Bot Version:', value=self.bot.version)
        embed.add_field(name='Python Version:', value=pythonVersion)
        embed.add_field(name='nextcord.Py Version', value=npyVersion)
        embed.add_field(name='Total Guilds:', value=serverCount)
        embed.add_field(name='Total Users:', value=memberCount)
        embed.add_field(name='Shard ID:', value=shard_id)
        embed.add_field(name='Shard Ping:', value=shard_ping)
        embed.add_field(name='Shard Servers:', value=shard_servers)
        embed.add_field(name='Bot Developers:', value=self.bot.owner_id)

        embed.set_footer(text=f"{ctx.author.guild.name} | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name, icon_url=self.bot.user.display_avatar)

        await ctx.send(embed=embed, view=view)


def setup(bot):
    bot.add_cog(About(bot))      
