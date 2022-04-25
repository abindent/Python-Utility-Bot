from rapidfuzz import fuzz, process
from typing import List, Tuple

import nextcord
from nextcord.ext import commands, menus

from bot import client as helpBot

from util.messages import DeleteMessage
from util.constants import Emojis, Icons, Client



class HelpPageSource(menus.ListPageSource):
    """Page source for dividing the list of tuples into pages and displaying them in embeds"""

    def __init__(self, help_command: "NewHelpCommand", data: List[Tuple[str, str]]):
        self._help_command = help_command
        # you can set here how many items to display per page
        super().__init__(data, per_page=4)

    async def format_page(self, menu: menus.ButtonMenuPages, entries: List[Tuple[str, str, str]]):
        """
        Returns an embed containing the entries for the current page
        """
        prefix = self._help_command.context.clean_prefix
        invoked_with = self._help_command.invoked_with
        # create embed
        embed = nextcord.Embed(title="Command Help", colour=self._help_command.COLOUR)
        embed.set_author(
            name=Client.name, icon_url=Icons.questionmark)
        embed.description = (
            f'Use `{prefix}{invoked_with} command` for more info on a command.\n'
            f'Use `{prefix}{invoked_with} category` for more info on a category.'
        )
        # add the entries to the embed
        for entry in entries:
            embed.add_field(name=entry[0], value=entry[1], inline=False)
        # set the footer to display the page number
        embed.set_footer(text=f'Page {menu.current_page + 1}/{self.get_max_pages()}')
        return embed


class HelpButtonMenuPages(menus.ButtonMenuPages):
    """Subclass of ButtonMenuPages to add an interaction_check"""
    FIRST_PAGE = Emojis.FIRST_EMOJI
    LAST_PAGE = Emojis.LAST_EMOJI
    PREVIOUS_PAGE = Emojis.LEFT_EMOJI
    NEXT_PAGE = Emojis.RIGHT_EMOJI
    STOP = Emojis.trashcan
    def __init__(self, ctx: commands.Context, **kwargs):
        super().__init__(**kwargs)
        self._ctx = ctx

    async def interaction_check(self, interaction: nextcord.Interaction) -> bool:
        """Ensure that the user of the button is the one who called the help command"""
        if self._ctx.author == interaction.user:
            return True
        else:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False


class NewHelpCommand(commands.MinimalHelpCommand):
    """Custom help command override using embeds and button pagination"""

    # embed colour
    COLOUR = nextcord.Colour.blurple()

    
    def get_command_signature(self, command: commands.core.Command):
        """Retrieves the signature portion of the help page."""
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

    async def command_not_found(self, string):
        embed = nextcord.Embed(title=f"Cannot find any command names : {string}", color=nextcord.Color.red())
        await self.get_destination().send(embed=embed, view=DeleteMessage(self.context))

    async def subcommand_not_found(self, command, string):
         embed = nextcord.Embed()
         embed.color = nextcord.Color.red()

         if isinstance(command, commands.Group) and len(command.all_commands) > 0:
           embed.title =  f'Command "{command.qualified_name}" has no subcommand named {string}'
         
         else:
            embed.title = f'Command "{command.qualified_name}" has no subcommands.'
      
         await self.get_destination().send(embed=embed, view=DeleteMessage(self.context))

    async def send_bot_help(self, mapping: dict):
        """implements bot command help page"""
        prefix = self.context.clean_prefix
        invoked_with = self.invoked_with
        embed = nextcord.Embed(title=f"{Client.name} Commands", colour=self.COLOUR)
        embed.set_author(
            name=Client.name, icon_url=Icons.questionmark)
        embed.description = (
            f'Use `{prefix}{invoked_with} command`  for more info on a command.\n'
            f'Use `{prefix}{invoked_with} category`  for more info on a category.'
        )

        # create a list of tuples for the page source
        embed_fields = []
        for cog, commands in mapping.items():
            emoji = getattr(cog, "COG_EMOJI", "")
            name = "No Category" if cog is None else f"{emoji} {cog.qualified_name}"
            filtered = await self.filter_commands(commands, sort=True)
            if filtered:
                # \u2002 = en space
                value = "\u2002".join(f"`{prefix}{c.name}`" for c in filtered)
                if cog and cog.description:
                    value = f"*{cog.description}*\n{value}\n"
                # add (name, value) pair to the list of fields
                embed_fields.append((name, value))

        # create a pagination menu that paginates the fields
        pages = HelpButtonMenuPages(
            ctx=self.context,
            source=HelpPageSource(self, embed_fields),
            delete_message_after=True
        )
        await pages.start(self.context)

    async def send_cog_help(self, cog: commands.Cog):
        """implements cog help page"""
        
        emoji = getattr(cog, "COG_EMOJI", "")
                
        embed = nextcord.Embed(
            title=f"{emoji}{cog.qualified_name} Commands",
            description=f'*{cog.description or "No Description Found"}*',
            colour=self.COLOUR,
        )
        embed.set_author(name=Client.name, icon_url=Icons.questionmark)
            

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(
                name=f"`{self.get_command_signature(command)}`",
                value=f'*{command.description or "No Description Found"}*',
                inline=False,
            )
        embed.set_footer(
            text=f"Use {self.context.clean_prefix}help [command] for more info on a command."
        )
        await self.get_destination().send(embed=embed, view=DeleteMessage(self.context))

    async def send_group_help(self, group: commands.Group):
        """implements group help help page"""
        embed = nextcord.Embed(title=f"Command {group.qualified_name}", colour=self.COLOUR)
        embed.set_author(
            name=Client.name, icon_url=Icons.questionmark)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(
                    name=f"`{self.get_command_signature(command)}`",
                    value=f'*{command.description or "There is no description."}*',
                    inline=False,
                )

        await self.get_destination().send(embed=embed, view=DeleteMessage(self.context))

    # Use the same function as group help for command help
    async def send_command_help(self, command: commands.command):
       
        """implements group help page and command help page"""
        aliase = str(", ").join(self.context.clean_prefix + aliases for aliases in command.aliases)

        embed = nextcord.Embed(title=f"Command {command.qualified_name}", description=f"```elm\n Syntax: {self.get_command_signature(command)}```", colour=self.COLOUR)
        embed.set_author(name=Client.name, icon_url=Icons.questionmark)
        
        embed.add_field(name=f"{command.qualified_name}", value=f'{command.description if command.description else "No Description Found"}', inline=False)

        if aliase:
           embed.add_field(name="Can also use:", value=f"`{aliase}`", inline=False)
               
        embed.set_footer(text=f"{Client.name} ▶️ {command.qualified_name}", icon_url=Icons.questionmark) 

        await self.get_destination().send(embed=embed, view=DeleteMessage(self.context))    
       
  

class Help(commands.Cog, name="Help"):
    """Displays help information for commands and cogs"""

    COG_EMOJI = "<:help:955474363786878986>"

    def __init__(self, bot: commands.Bot):
        self.__bot = bot
        self.__original_help_command = bot.help_command
        bot.help_command = NewHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        self.__bot.help_command = self.__original_help_command              
