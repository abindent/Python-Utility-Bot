import os, json, nextcord, datetime, random
from nextcord import ChannelType, SlashOption
from nextcord.abc import GuildChannel
from nextcord.ext import commands, activities, application_checks


class MakeLink(nextcord.ui.View):
    def __init__(self, link: str):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Join Game", url=f"{link}"))

# DropDown View
# SELECT MENUS AND BUTTONS


class DropDown(nextcord.ui.Select):
    def __init__(self):
        options = [
            nextcord.SelectOption(
                label="Python", description="Python is a user friendly language born from C language."),
            nextcord.SelectOption(
                label="JavaScript", description="JavaScript is a very popular language can be executed by the browser."),
            nextcord.SelectOption(
                label="HTML", description="HTML is mandatory while building websites."),
            nextcord.SelectOption(
                label="CSS", description="Raw HTML looks bad, so CSS styles and decorates it."),
            nextcord.SelectOption(
                label="PHP", description="PHP is also a very popular language (used in Wordpress).")
        ]
        super().__init__(placeholder="Select Your Language",
                         min_values=1, max_values=1, options=options)

    async def callback(self, interaction: nextcord.Interaction):
        if self.values[0] == "Python":
            langembed = nextcord.Embed(
                title=f":wave: Hi {interaction.user.name}", description="**You have choosed <:python:935932879714779227> python.**")

            langembed.set_author(
                name="OpenSourceGames Utility", icon_url=interaction.client.user.display_avatar, url="https://python.org")
            langembed.add_field(name="__ABOUT__", value="***Python is an interpreted high-level general-purpose programming language. Its design philosophy emphasizes code readability with its use of significant indentation. Its language constructs as well as its object-oriented approach aim to help programmers write clear, logical code for small and large-scale projects***")

            await interaction.response.edit_message(embed=langembed)

        if self.values[0] == "JavaScript":
            langembed = nextcord.Embed(
                title=f":wave: Hi {interaction.user.name}", description="**You have choosed <:JS:935933057800757318> javascript.**")

            langembed.set_author(
                name="OpenSourceGames Utility", icon_url=interaction.client.user.display_avatar, url="https://javascript.com")
            langembed.add_field(name="__ABOUT__", value="***JavaScript, often abbreviated JS, is a programming language that is one of the core technologies of the World Wide Web, alongside HTML and CSS. Over 97% of websites use JavaScript on the client side for web page behavior, often incorporating third-party libraries.***")
            await interaction.response.edit_message(embed=langembed)

        if self.values[0] == "HTML":
            langembed = nextcord.Embed(
                title=f":wave: Hi {interaction.user.name}", description="**You have choosed <:html:935933258439483442> HTML.**")

            langembed.set_author(
                name="OpenSourceGames Utility", icon_url=interaction.client.user.display_avatar, url="https://html.com")
            langembed.add_field(name="__ABOUT__", value="***The HyperText Markup Language, or HTML is the standard markup language for documents designed to be displayed in a web browser. It can be assisted by technologies such as Cascading Style Sheets (CSS) and scripting languages such as JavaScript. ... HTML elements are the building blocks of HTML pages.***")
            await interaction.response.edit_message(embed=langembed)
        if self.values[0] == "CSS":
            langembed = nextcord.Embed(
                title=f":wave: Hi {interaction.user.name}", description="**You have choosed <:css:935935867468533830> CSS.**")

            langembed.set_author(
                name="OpenSourceGames Utility", icon_url=interaction.client.user.display_avatar, url="https://g.co/kgs/83EKjE")
            langembed.add_field(name="__ABOUT__", value="***Cascading Style Sheets is a style sheet language used for describing the presentation of a document written in a markup language such as HTML. CSS is a cornerstone technology of the World Wide Web, alongside HTML and JavaScripts.***")
            await interaction.response.edit_message(embed=langembed)
        if self.values[0] == "PHP":
            langembed = nextcord.Embed(
                title=f":wave: Hi {interaction.user.name}", description="**You have choosed <:php:935937346799546408> PHP.**")

            langembed.set_author(
                name="OpenSourceGames Utility", icon_url=interaction.client.user.display_avatar, url="https://php.net/")
            langembed.add_field(name="__ABOUT__", value="***PHP is a general-purpose scripting language geared towards web development. It was originally created by Danish-Canadian programmer Rasmus Lerdorf in 1994. The PHP reference implementation is now produced by The PHP Group.***")
            await interaction.response.edit_message(embed=langembed)


class DropDownView(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(DropDown())


class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

   
    # SLASH COMMAND

    # 8ball Slash Command
    @nextcord.slash_command(name="8ball", description="Let the 8 Ball Predict!\nthe future")
    async def eightball(self, interaction: nextcord.Interaction, *, question=SlashOption(name="question", description="Enter your question")):
        responses = [
            'It is certain.',
            'It is decidedly so.',
            'Without a doubt.',
            "I'm feeling well",
            'Yes - definitely.',
            'You may rely on it.',
            'As I see it yes.',
            'Most likely.',
            'Outlook good.',
            'Yes.',
            'Signs point to yes.',
            'Reply hazy, try again.',
            'Better not tell you now.',
            'Concentrate and ask again.',
            "Don't count on it.",
            'I cannot predict now.',
            'My reply is no.',
            'My sources say no.',
            'Outlook not so good.',
            'VEry doubtfull.',
            'I am tired. *proceeds with sleeping*',
            'As I see it, yes.',
            'Yes.',
            'Positive',
            'From my point of view, yes',
            'Convinced.',
            'Most Likley.',
            'Chances High',
            'No.',
            'Negative.',
            'Not Convinced.',
            'Perhaps.',
            'Not Sure',
            'Mayby',
            'Im to lazy to predict.'
        ]
        await interaction.response.send_message(f":8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}", ephemeral=True)

    # TOGGLE COMMANDS SLASH COMMAND
    @nextcord.slash_command(name="toggle", description="Enables a Disabled Command and Disables an Enabled Command.")
    @application_checks.has_guild_permissions(administrator=True)
    async def toggle(self, interaction: nextcord.Interaction, *, command=SlashOption(name="command", description="Enter the name of the command you want to diable.")):
        command = self.bot.get_command(command)

        if command == None:
            await interaction.response.send_message(f"Requested command 😞 {command.name} not found.**", ephemeral=True)
        elif command == "toggle":
            await interaction.response.send_message(f"{command.name} cannot be disabled.", ephemeral=True)
        else:
            command.enabled = not command.enabled
            ternary = "enabled" if command.enabled else "disabled"
            togglembed = nextcord.Embed(
                title=f"Toggled {command.qualified_name}", description=f"**The {command.qualified_name} command has been {ternary}**")
            togglembed.set_author(
                name="OpenSourceGames Utility", icon_url=interaction.client.user.display_avatar)
            togglembed.set_footer(
                text=f"Command requested by {interaction.user.name}")
            await interaction.response.send_message(embed=togglembed, ephemeral=True)

    # Lang Slash Command

    @nextcord.slash_command(name="lang", description="Choose your language and learn about it.")
    async def _lang(self, interaction: nextcord.Interaction):
        view = DropDownView()
        langembed = nextcord.Embed(
            title=f":wave: Hi {interaction.user.name}", description=f"**Please choose your language from the opion below.**")
        langembed.set_author(
            name="OpenSourceGames Utility", icon_url=interaction.client.user.display_avatar,)
        langembed.set_footer(
            text=f"Command requested by {interaction.user.name}")
        await interaction.response.send_message(embed=langembed, view=view, ephemeral=True)

    # Clear Slash Command

    @nextcord.slash_command(name="clear", description="Clears messages")
    @application_checks.has_guild_permissions(administrator=True)
    async def clear(self, interaction: nextcord.Interaction, amount: int = SlashOption(name="amount", description="Enter the amount of the messages.")):
        if amount > 1000:
            await interaction.response.send_message('Cannot delete more than 1000 messages.', ephemeral=True)
        else:
            new_count = {}
            messages = await interaction.channel.history(limit=amount).flatten()
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
            await interaction.channel.purge(limit=amount)
            await interaction.response.send_message(f"Successfully cleared `{deleted_messages} messages`\n\n{new_message}", ephemeral=True)

    # Ping Slash Command
    @nextcord.slash_command(name="ping", description="Returns the latency of the bot")
    async def ping(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(f"Pong! Latency is {self.bot.latency}ms", ephemeral=True)
  
    # Activity Slash Command
    @nextcord.slash_command(name="activity", description="Creates an activity in your channel.")
    async def activity_slash(self, interaction: nextcord.Interaction, activity: str = SlashOption(name="activity", description="Choose the activity", choices={"Poker Night (Requires Boost Level 1)": "755827207812677713", "Betrayal.io": "773336526917861400", "Fishington (broken)": "814288819477020702", "Chess In The Park (Requires Boost Level 1)": "832012774040141894", "Checkers In The Park (Requires Boost Level 1)": "832013003968348200", "Youtube Watch Together": "880218394199220334",  "Skecth Heads (new Doddle Crew)": "902271654783242291",  "Word Snacks": "879863976006127627", "SpellCast (Requires Boost Level 1)": "852509694341283871", "Letter League (formerly Letter Tile) (Requires Boost Level 1)": "879863686565621790", "Awkword (Requires Boost Level 1)": "879863881349087252", "Blazing 8s (New! Formerly Ocho) (Requires Boost Level 1)": "832025144389533716", "Sketch Artist": "879864070101172255", "Putt Party":"945737671223947305"}), channel: GuildChannel = SlashOption(channel_types=[ChannelType.voice])):
        target_id = activity.replace('"', "")
       
        invite_link = await channel.create_activity_invite(activities.Activity.custom, activity_id=target_id)
        embed = nextcord.Embed(
            title=":rocket: Discord Activity", description=f"{interaction.user.mention} has created activity in {channel.name}.", color=nextcord.Color.green())
        embed.add_field(
            name="What is it?",
            value="**__According to Discord__**\nLike playing games with your friends, and want to make it easier to organize them? We got your back! We’re starting a new experiment where some servers will get access to Activities on Discord. These Activities will appear inside a voice channel, and anyone on Desktop in the voice channel can join and play together instantly inside Discord!")
        embed.set_thumbnail(
            url="https://i.ytimg.com/vi_webp/POMIDMK6WfM/maxresdefault.webp")
        await interaction.response.send_message(embed=embed, view=MakeLink(invite_link))

def setup(bot):
    bot.add_cog(Slash(bot))
