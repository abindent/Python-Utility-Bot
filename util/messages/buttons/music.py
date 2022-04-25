import nextcord, wavelink
from util.constants import Emojis

class MusicController(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.paused =True

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji=Emojis.mute)
    async def mute(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):

        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title=f"📢 Your are not playing a song.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.set_volume(volume=0)
        await interaction.response.send_message("Successfully muted the player.", ephemeral=True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji=Emojis.pause)
    async def pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
      if self.paused:
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        embed = nextcord.Embed(
            title=f"📢 | {Emojis.pause} Paused the player.", color=0x91cd0e)
        await vc.pause()
        self.pause.emoji = Emojis.resume
        self.pause.style = nextcord.ButtonStyle.green
        self.paused = False
        await interaction.message.edit(view=self)
        await interaction.response.send_message(embed=embed, ephemeral=True)

      else:
            if not interaction.guild.voice_client:
              embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
              await interaction.response.send_message(embed=embed, ephemeral=True)

            elif not getattr(interaction.user.voice, "channel", None):
              embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
              await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
              vc: wavelink.Player = interaction.guild.voice_client

            embed = nextcord.Embed(
              title=f"📢 | ⏯️ Resumed the player.", color=0x91cd0e)
            await vc.resume()
            self.pause.emoji = Emojis.pause
            self.pause.style = nextcord.ButtonStyle.secondary
            self.paused =True
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=embed, ephemeral=True)


    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji=Emojis.halfvolume)
    async def halfvolume(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.set_volume(volume=50)
        await interaction.response.send_message("Successfully set you volume to `50%`", ephemeral=True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji=Emojis.fullvolume)
    async def fullvolume(self, button: nextcord.ui.Button, interaction=nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.set_volume(volume=100)
        await interaction.response.send_message("Successfully set you volume to `100%`", ephemeral=True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji=Emojis.loop)
    async def loop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)

        if vc.loop:
            return await interaction.response.send_message(f"Enabled {Emojis.loop} Loop", ephemeral=True)
        else:
            return await interaction.response.send_message(f"Disabled {Emojis.loop} Loop", ephemeral=True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji=Emojis.closeConnection)
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        await vc.stop()
