# Importing Modules
import discord
from discord import app_commands
from discord.ext import commands

# Importing database
from utils.databases.thread import SupportDB

# Utilty
from typing import List


# Support


class Support(commands.Cog, name="Support"):

    """ 📧Support : A group of commands to create support threads for reasons."""

    COG_EMOJI = "📧"

    def __init__(self, bot: commands.AutoShardedBot) -> None:
        self.bot = bot
        self.description = "A group of commands to manage threads for reasons."
        self.db = SupportDB(self.bot)

    group = app_commands.Group(
        name="support", description="A group of commands for getting support.")

    async def setup(self, interaction: discord.Interaction, support_channel_id, log_channel_id) -> None:

        data = await self.db.create_table(guild_id=interaction.guild.id, support_channel_id=support_channel_id, log_channel_id=log_channel_id)
        await interaction.response.send_message("✅ Successfully set up the channels", ephemeral=True)


    @group.command(name="setup", description="Runs a setup function")
    @app_commands.describe(support_channel="Sets the support channel.", log_channel="Sets the log channel")
    async def run_setup(self, interaction: discord.Interaction, support_channel: discord.TextChannel, log_channel: discord.TextChannel) -> None:
        if support_channel.id == log_channel.id:
            await interaction.response.send_message(":x: Sorry support channel and log channel must be different!", ephemeral=True)

        else:
            await self.setup(interaction=interaction, support_channel_id=support_channel.id, log_channel_id=log_channel.id)

    @group.command(name="create", description="Creates a thread for support")
    @app_commands.describe(problem="Explain in short that why you need help.")
    async def add_thread(self, interaction: discord.Interaction, problem: str = "Unidentified reason") -> None:
        data = await self.db.get_data(interaction.guild.id)
        if data:

            support_channel = interaction.guild.get_channel_or_thread(
                int(data["support_channel"]))
            existChannel = discord.utils.get(
                interaction.guild.threads, name=f"📧-{interaction.user.name}-support")
            if existChannel:
                await interaction.response.send_message(f":x: Your already have an existing support thread. Click here to visit {existChannel.jump_url}", ephemeral=True)

            else:
                channel = await support_channel.create_thread(name=f"📧-{interaction.user.name}-support", type=discord.ChannelType.private_thread)
                embed = discord.Embed(color=discord.Color.green(
                ), title="📧 Support Thread", description=f"Reason: ```ml\n{problem}``` ",)
                await interaction.response.send_message(f"✅ Successfully added you to the thread. Click here to join {channel.jump_url}", ephemeral=True)
                await channel.send(content=f"Howdy {interaction.user.mention}!!", embed=embed)

        else:
            await interaction.response.send_message(":x: No setup was found. please configure one by running `/support setup`")

    @group.command(name="delete", description="Deletes an existng support thread if you don't need that.")
    @app_commands.describe(reason="Enter your support thread id")
    async def del_thread(self, interaction: discord.Interaction, reason: str = "Nothing Specified") -> None:
        data = await self.db.get_data(interaction.guild.id)
        if data:

            channel = discord.utils.get(
                interaction.guild.threads, name=f"📧-{interaction.user.name}-support")

            if channel:
                embed = discord.Embed(color=discord.Color.green(
                ), title="📧 Deleted Support Thread", description=f"**User:** {interaction.user.mention} \n **Reason:** ```ml\n{reason}``` ",)
                await channel.delete()
                await interaction.guild.get_channel_or_thread(int(data["log_channel"])).send(content=f"{interaction.user.mention}", embed=embed)

        else:
            await interaction.response.send_message(":x: No setup was found. please configure one by running `/support setup`")
