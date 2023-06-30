# Importing Modules
import discord
from discord import app_commands
from discord.ext import commands
# Support Thread


class Thread(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True

    @discord.ui.button(style=discord.ButtonStyle.primary, emoji="")
    async def lock_thread(self):
        pass 