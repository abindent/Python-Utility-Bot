import nextcord, json, os, asyncio, humanfriendly, aiohttp, datetime
import nextwave 

from nextcord.ext import commands
from utils.delbtn import DelBtn as MessageDelete


class MusicController(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
    
    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True
    
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji="🔈")
    async def mute(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
              
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title="🔊 Set Volume Music", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="🔊 Set Volume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: nextwave.Player = interaction.guild.voice_client

    
        await vc.set_volume(volume=0)
        await interaction.response.send_message("Successfully muted the player.", ephemeral=True)   
                                       
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji="<:emoji_2:900445202899140648>")
    async def pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
       
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title="⏸️ Pause Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏸️ Pause Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: nextwave.Player = interaction.guild.voice_client

        embed = nextcord.Embed(title="⏸️ Pausing Music..",
                            description=f"📢 | ⏸️ Paused the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                        icon_url=interaction.client.user.display_avatar)
        await vc.pause()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, emoji="<:emoji_1:900445170103889980>")
    async def resume(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title="⏯️ Resume Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏯️ Resume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: nextwave.Player = interaction.guild.voice_client

        embed = nextcord.Embed(title="⏯️ Resuming Music..",
                               description=f"📢 |⏯️ Resumed the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         icon_url=interaction.client.user.display_avatar)
        await vc.resume()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji="🔉")
    async def halfvolume(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
              
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title="🔊 Set Volume Music", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="🔊 Set Volume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: nextwave.Player = interaction.guild.voice_client

    
        await vc.set_volume(volume=50)
        await interaction.response.send_message("Successfully set you volume to `50%`", ephemeral=True)    
    
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji="🔊")
    async def fullvolume(self, button: nextcord.ui.Button, interaction= nextcord.Interaction):
              
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title="🔊 Set Volume Music", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="🔊 Set Volume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: nextwave.Player = interaction.guild.voice_client

    
        await vc.set_volume(volume=100)
        await interaction.response.send_message("Successfully set you volume to `100%`", ephemeral=True)   

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji="<:emoji_7:900445329982369802>")
    async def loop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title="<:loop:950322712805507104> Loop Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                                icon_url=interaction.client.user.display_avatar)
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="<:loop:950322712805507104> Loop Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                                icon_url=interaction.client.user.display_avatar)
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: nextwave.Player = interaction.guild.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)

        if vc.loop:
            return await interaction.response.send_message("Enabled <:loop:950322712805507104> Loop", ephemeral=True)        
        else:
            return await interaction.response.send_message("Disabled <:loop:950322712805507104> Loop", ephemeral=True)        
      

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji="<a:closeimout:848156958834032650>")
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title="⏸ Stop Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏸ Stop Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: nextwave.Player = interaction.guild.voice_client
        
        await vc.stop()

            
        
        
class Music(commands.Cog):

    COG_EMOJI = "🎶"
    
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await nextwave.NodePool.create_node(bot=self.bot, host="connect.freelavalink.ga", port=443, password="www.freelavalink.ga", https=True)


    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: nextwave.Node):
        print(f"Node <{node.identifier}> is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: nextwave.Player, track: nextwave.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.stop(), await vc.play(track), await songplayembed.edit(view=MusicController(self._global_ctx))

        if vc.queue.is_empty:
            return await vc.stop() , await songplayembed.edit(view=MessageDelete(self._global_ctx))
             

        next_song = vc.queue.get()

        view = MusicController(self._global_ctx)
        embed = nextcord.Embed(title="▶️ Playing Music..",
                               description=f"📢 | Now Playing `{next_song.title}` by {next_song.author} \n **LINK:** {next_song.uri}", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         icon_url=self.bot.user.display_avatar)
        embed.add_field(
            name="Duration", value=humanfriendly.format_timespan(next_song.duration))
        embed.set_image(url=next_song.thumbnail)
        await vc.stop()
        await vc.play(next_song)
        await songplayembed.edit(embed=embed, view=view)


    @commands.command(name="play", description="▶️ Plays a song for you that you want.", usage="<song name>")
    async def play(self, ctx: commands.Context, *, search: nextwave.YouTubeTrack):
        if not ctx.voice_client:
            vc: nextwave.Player = await ctx.author.voice.channel.connect(cls=nextwave.Player)

        elif not ctx.author.voice:
            embed = nextcord.Embed(
                title="▶️ Play Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            return await ctx.send(embed=embed)

        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            embed = nextcord.Embed(
                title="▶️ Play Music", description="📢 | Joining your voice channel...", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            msg = await ctx.send(embed=embed)
            vc: nextwave.Player = ctx.voice_client
            await vc.move_to(ctx.author.voice.channel)
            return msg
            await asyncio.sleep(7)
            msg.delete()

            
        else:
            vc: nextwave.Player = ctx.voice_client

        if vc.queue.is_empty and not vc.is_playing():

            view = MusicController(ctx)
            embed = nextcord.Embed(title="▶️ Playing Music..",
                                description=f"📢 | Now Playing `{search.title}` by {search.author} \n **LINK:** {search.uri}", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            icon_url=self.bot.user.display_avatar)
            embed.add_field(name="Duration",
                            value=humanfriendly.format_timespan(search.duration))
            embed.set_image(url=search.thumbnail)
            await vc.play(search)
            global songplayembed 
            songplayembed = await ctx.send(embed=embed, view=view)

        else:
            await vc.queue.put_wait(search)
            embed = nextcord.Embed(title="▶️ Added Music to the queue.",
                                description=f"📢 | Now Playing `{search.title}` by {search.author} \n **LINK:** {search.uri}", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            icon_url=self.bot.user.display_avatar)
            embed.add_field(name="Duration",
                            value=humanfriendly.format_timespan(search.duration))
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
  
        vc.ctx = ctx
        self._global_ctx = ctx
        setattr(vc, "loop", False)

    @commands.command(name="pause", description="⏸️ Pauses playing song.")
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="⏸️ Pause Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        elif not ctx.author.voice:
            embed = nextcord.Embed(
                title="⏸️ Pause Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: nextwave.Player = ctx.voice_client

        if ctx.author is self._global_ctx.author:
            embed = nextcord.Embed(title="⏸️ Pausing Music..",
                                   description=f"📢 | ⏸️ Paused the player.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            await vc.pause()
            message = await ctx.send(embed=embed, view=None)
            await asyncio.sleep(5)
            await message.delete()
        
        else:
            msg = await ctx.send(":no_entry: This song is not yours, so you can't pause it.")
            await asyncio.sleep(5)
            await msg.delete         

    @commands.command(name="resume", description="⏯️ Resumes playing song.")
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="⏯️ Resume Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏯️ Resume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: nextwave.Player = ctx.voice_client
          
        if ctx.author is self._global_ctx.author:  
           embed = nextcord.Embed(title="⏸️ Resuming Music..",
                                  description=f"📢 | ⏯️ Resumed the player.", color=0x91cd0e)
           embed.set_author(name="OpenSourceGames Utility",
                            icon_url=self.bot.user.display_avatar)
           await vc.resume()
           message = await ctx.send(embed=embed)
           await asyncio.sleep(5)
           await message.delete()
        else:
            msg = await ctx.send(":no_entry: This song is not yours, so you can't resume it.")
            await asyncio.sleep(5)
            await msg.delete         

    @commands.command(name="loop", description="Enables Looping")
    async def loop(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="<:loop:950322712805507104> Loop Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="<:loop:950322712805507104> Loop Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: nextwave.Player = ctx.voice_client
     
        if ctx.author is self._global_ctx.author:
         try:
             vc.loop ^= True
         except Exception:
             setattr(vc, "loop", False)
 
         if vc.loop:
             return await ctx.send("Enabled <:loop:950322712805507104> Loop")        
         else:
             return await ctx.send("Disabled <:loop:950322712805507104> Loop")        
        else:
            msg = await ctx.send(":no_entry: This song is not yours, so you can't control the <:loop:950322712805507104> loop.")
            await asyncio.sleep(5)
            await msg.delete            
        

    @commands.command(name="queue", description="Queues a song..")
    async def queue(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="⏯️ Resume Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏯️ Resume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message,await asyncio.sleep(5),await message.delete()

        else:
            vc: nextwave.Player = ctx.voice_client    

        if vc.queue.is_empty:
            embed = nextcord.Embed(
                title="➕ Queue Music..", description=f"📢 | The queue is empty.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed, view=MessageDelete())
            await asyncio.sleep(7)
            await message.delete()    

        embed = nextcord.Embed(
                title="➕ Queue Music..", description=f"📢 | The queue is given below.", color=0x91cd0e)
        queue = vc.queue.copy()
        song_count = 0
        for song in queue:
            song_count +=1
            embed.add_field(name="‏‏‎ ", value=f"**{song_count})** {song.title}", inline=False)

        await ctx.send(embed=embed, view=MessageDelete())    

    @commands.command(name="stop", description="⏸ Stops playing song.")
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="⏸ Stop Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏸ Stop Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        else:
            vc: nextwave.Player = ctx.voice_client

        embed = nextcord.Embed(title="⏸ Stopping Music..",
                               description=f"📢 | ⏸️ Stoped the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         icon_url=self.bot.user.display_avatar)
        await vc.stop()
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="disconnect", aliases=["vcdisconnect"], description="🔌 Disconnects from the vc.")
    async def vcdisconnect(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="🔌 Disconnect Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="🔌 Disconnect Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: nextwave.Player = ctx.voice_client

        embed = nextcord.Embed(title="🔌 Disconnecting Music..",
                               description=f"📢 |🔌 Disconnected Successfully.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         icon_url=self.bot.user.display_avatar)
        await vc.disconnect()
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="connect", description="🔌 Connects from the vc.")
    async def connect(self, ctx: commands.Context):
        if not ctx.voice_client:
            vc: nextwave.Player = await ctx.author.voice.channel.connect(cls=nextwave.Player)

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="🔌 Connect Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        else:
            vc: nextwave.Player = ctx.voice_client

        embed = nextcord.Embed(title="🔌 Connecting Music..",
                               description=f"📢 |🔌 Connected Successfully.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         icon_url=self.bot.user.display_avatar)
        await vc.connect(timeout=14, reconnect=True)
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="volume", aliases=["setvolume", "changevolume"], descrtiption="Sets the volume of the player.")
    async def setvolume(self, ctx: commands.Context, *, volume: int):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="🔊 Volume Music", description="📢 | I am not in a voice channel.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(4), message.delete()

        elif not ctx.author.voice:
            embed = nextcord.Embed(
                title="🔊 Volume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(4), message.delete()

            
        else:
            vc: nextwave.Player = ctx.voice_client
        
        if ctx.author is self._global_ctx.author:

            if volume > 100:
                msg = await ctx.send(":angry: It's too much high.")    
                await asyncio.sleep(4)
                await msg.delete()

            elif volume < 0:
                msg = await ctx.send(":angry: It's too low.")    
                await asyncio.sleep(4)
                await msg.delete()
            
            else:   

                msg = await ctx.send(f"Set your 🔊 volume to `{volume}%`")   
                return await vc.set_volume(volume), msg,  await asyncio.sleep(3), await msg.delete()

        else:
            msg = await ctx.send(":no_entry: This song is not yours, so you can't control it's 🔊 volume.")
            await asyncio.sleep(5)
            await msg.delete()

    @commands.command(name="nowplaying", aliases=["np", "songinfo"], description="Shows the info about the currently playing song.")
    async def nowplaying(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="🔊 Now Playing Music", description="📢 | I am not in a voice channel.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(4), message.delete()

        elif not ctx.author.voice:
            embed = nextcord.Embed(
                title="🔊 Now Playing Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(4), message.delete()

            
        else:
            vc: nextwave.Player = ctx.voice_client

        if not vc.is_playing():
            embed = nextcord.Embed(
                title="🔊 Now Playing Music", description="📢 | You are not even playing a music.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(4), message.delete()

        embed = nextcord.Embed(title="🎶 Now Playing", description=f"🎶 | I am playing `{vc.track.title}` by {vc.track.author} \n **VIDEO LINK:** {vc.track.uri}", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                        icon_url=self.bot.user.display_avatar)
        embed.add_field(name="Duration",
                        value=humanfriendly.format_timespan(vc.track.length))
        embed.set_image(url=vc.track.thumbnail)
        await ctx.send(embed=embed, view=MessageDelete())    



    @commands.command(name="lyrics", description="Sends the lyrics of the song.", usage="<song name>")
    async def lyrics(self, ctx,*, name: str):
        url = "https://some-random-api.ml/lyrics?title="
        player = nextwave.Player 
        lyrics = name or player.queue.current_track.title

        async with ctx.typing():
            async with aiohttp.request("GET", url+name, headers={}) as r :
                try:
                    if not r.status == 200:
                        view = MessageDelete()
                        embed = nextcord.Embed(title="Aw Snap!",description="I wasn't able to find the lyrics of that song.",color = 0xa3a3ff)
                        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/830818408550629407/839555682436251698/aw_snap_large.png')
                        await ctx.send(embed=embed, view=view)

                    data = await r.json()
                    if len(data["lyrics"]) > 2000:
                        view = MessageDelete()
                        return await ctx.send(f"The lyrcis exceeded the limit so here is the link for the lyrics: <{data['links']['genius']}>", view=view)

                    view = MessageDelete()
                    embed = nextcord.Embed(title=data["title"], description=data["lyrics"], color=nextcord.Color.blue(), timestamp=datetime.datetime.utcnow()) 
                    embed.set_author(name=data["author"], icon_url=self.bot.user.display_avatar)
                    embed.set_thumbnail(url=data["thumbnail"]["genius"])  
                    await ctx.send(embed=embed, view=view) 

                except KeyError:
                    pass
                           

def setup(bot):
    bot.add_cog(Music(bot))
