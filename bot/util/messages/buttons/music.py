import nextwave

import nextcord
from nextcord.ext import commands

from util.constants import Emojis


class MusicController(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.paused = True
        self.halfvolume = False

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True
       

    @nextcord.ui.button(style=nextcord.ButtonStyle.blurple, emoji=Emojis.list_emoji)
    async def show_queue_list(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: nextwave.Player = interaction.guild.voice_client

        if vc.queue.is_empty:
            embed = nextcord.Embed(
                title=f"📢 | The queue is empty.", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        embed = nextcord.Embed(
            title=f"📢 | The queue is given below.", color=0x91cd0e)
        queue = vc.queue.copy()

        song_count = 0
        for song in queue:
            song_count += 1
            embed.add_field(
                name="‏", value=f"**{song_count})** {song.title}", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji=Emojis.shuffle)
    async def shuffle(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
         if not interaction.guild.voice_client:
             embed = nextcord.Embed(
                 title=f"📢 | Your are not playing a song.", color=0x91cd0e)
             await interaction.response.send_message(embed=embed, ephemeral=True)
         elif not getattr(interaction.user.voice, "channel", None):
             embed = nextcord.Embed(
                 title=f"📢 | Join a voice channel please.", color=0x91cd0e)
             await interaction.response.send_message(embed=embed, ephemeral=True)
         else:
             vc: nextwave.Player = interaction.guild.voice_client
           
         if vc.queue.is_empty:
             embed = nextcord.Embed(title=f'{Emojis.shuffle} Your queue is empty', color=0xff0000)
             await interaction.response.send_message(embed=embed, ephemeral=True)  
         vc.queue.shuffle()
         embed = nextcord.Embed(title=f"{Emojis.shuffle} Shuffled the queue", color=0x91cd0e)
         await interaction.response.send_message(embed=embed, ephemeral=True)

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
                vc: nextwave.Player = interaction.guild.voice_client

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
                vc: nextwave.Player = interaction.guild.voice_client

            embed = nextcord.Embed(
                title=f"📢 | ⏯️ Resumed the player.", color=0x91cd0e)
            await vc.resume()
            self.pause.emoji = Emojis.pause
            self.pause.style = nextcord.ButtonStyle.secondary
            self.paused = True
            await interaction.message.edit(view=self)
            await interaction.response.send_message(embed=embed, ephemeral=True)

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
            vc: nextwave.Player = interaction.guild.voice_client

        await vc.set_volume(0)
        embed = nextcord.Embed(
            title=f'{Emojis.mute} | Muted the player Successfully.', color=0x91cd0e)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @nextcord.ui.button(label="100%", style=nextcord.ButtonStyle.green, emoji=Emojis.fullvolume)
    async def change_volume(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if self.halfvolume:
            if not interaction.guild.voice_client:
                embed = nextcord.Embed(
                    title=f"📢 | Your are not playing a song.", color=0x91cd0e)
                await interaction.response.send_message(embed=embed, ephemeral=True)

            elif not getattr(interaction.user.voice, "channel", None):
                embed = nextcord.Embed(
                    title=f"📢 | Join a voice channel please.", color=0x91cd0e)
                await interaction.response.send_message(embed=embed, ephemeral=True)

            else:
                vc: nextwave.Player = interaction.guild.voice_client

            button.label = "100%"
            button.emoji = Emojis.fullvolume
            button.style = nextcord.ButtonStyle.green
            self.halfvolume = False
            await interaction.message.edit(view=self)
            await vc.set_volume(50)
            embed = nextcord.Embed(
                title=f"{Emojis.fullvolume} Successfully set you volume to `50%`", color=0x91cd0e)
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
                vc: nextwave.Player = interaction.guild.voice_client

            button.label = "50%"
            button.emoji = Emojis.halfvolume
            button.style = nextcord.ButtonStyle.secondary
            self.halfvolume = True
            await interaction.message.edit(view=self)
            await vc.set_volume(100)
            embed = nextcord.Embed(
                title=f"{Emojis.fullvolume} Successfully set you volume to `100%`", color=0x91cd0e)
            await interaction.response.send_message(embed=embed, ephemeral=True)

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
            vc: nextwave.Player = interaction.guild.voice_client

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
            vc: nextwave.Player = interaction.guild.voice_client

        if not vc.queue.is_empty and vc.queue:
            vc.queue.clear()

        await vc.stop()
