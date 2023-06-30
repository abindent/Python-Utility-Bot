# Importing Modules
import discord
from discord import app_commands
from discord.ext import commands

# Support


class Support(commands.Cog, name="Support"):

    """ 📧Support : A group of commands to create support threads for reasons."""

    COG_EMOJI = "📧"

    def __init__(self, bot: commands.AutoShardedBot) -> None:
        self.bot = bot
        self.description = "A group of commands to manage threads for reasons."

    group = app_commands.Group(
        name="support", description="A group of commands for getting support.")

    @group.command(name="create", description="Creates a thread for support")
    @app_commands.describe(problem="Explain in short that why you need help.")
    async def add_thread(self, interaction: discord.Interaction, problem: str):

        try:
            support_channel = await interaction.guild.fetch_channel(957315994710343722)
            channel = await support_channel.create_thread(name=f"📧-{interaction.user.name}-support", type=discord.ChannelType.private_thread)

            await interaction.response.send_message(f"✅ Successfully added you to the thread. Click here to join {channel.jump_url}", ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"Something went wrong! {e}")