import nextcord, json, wavelink, os, asyncio, humanfriendly, aiohttp, datetime
from nextcord.ext import commands


class MessageDelete(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary,emoji="<:dustbin:949602736633167882>")
    async def on_stop(self, button, interaction: nextcord.Interaction):
        await interaction.message.delete()


class MusicController(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    async def interaction_check(self, interaction):
        if self.ctx.author !=interaction.user:
           await interaction.response.send_message("You haven't run the command.So you are not my author for this controller.",ephemeral=True
           return False
        return True                                           
  
    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)                                          
                                                           
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji="<:emoji_2:900445202899140648>")
    async def pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
       
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title="⏸️ Pause Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏸️ Pause Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        embed = nextcord.Embed(title="⏸️ Pausing Music..",
                            description=f"📢 | ⏸️ Paused the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                        url=interaction.client.user.display_avatar)
        await vc.pause()
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @nextcord.ui.button(style=nextcord.ButtonStyle.green, emoji="<:emoji_1:900445170103889980>")
    async def resume(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title="⏯️ Resume Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏯️ Resume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        embed = nextcord.Embed(title="⏯️ Resuming Music..",
                               description=f"📢 |⏯️ Resumed the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         url=interaction.client.user.display_avatar)
        await vc.resume()
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @nextcord.ui.button(style=nextcord.ButtonStyle.secondary, emoji="<:emoji_7:900445329982369802>")
    async def loop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed = nextcord.Embed(
                title="<:loop:950322712805507104> Loop Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                                url=interaction.client.user.display_avatar)
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="<:loop:950322712805507104> Loop Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                                url=interaction.client.user.display_avatar)
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

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
                             url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏸ Stop Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client

        for child in self.children:
            child.disabled = True
            await interaction.message.edit(view=self)
        await vc.stop()
        await vc.disconnect()


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="lava.link", port=80, password="dismusic")
    


    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")

    @commands.Cog.listener()
    async def on_waveink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.id}> is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.play(track)

        if vc.queue.is_empty:
            return await vc.stop() , await songplayembed.edit(view=MessageDelete())
             

        next_song = vc.queue.get()

        view = MusicController()
        embed = nextcord.Embed(title="▶️ Playing Music..",
                               description=f"📢 | Now Playing `{next_song.title}` by {next_song.author} \n **LINK:** {next_song.uri}", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         url=self.bot.user.display_avatar)
        embed.add_field(
            name="Duration", value=humanfriendly.format_timespan(next_song.duration))
        embed.set_image(url=next_song.thumbnail)
        await vc.stop()
        await vc.play(next_song)
        await songplayembed.edit(embed=embed, view=view)

    @commands.command(name="play", description="▶️ Plays a song for you that you want.")
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)

        elif not ctx.author.voice:
            embed = nextcord.Embed(
                title="▶️ Play Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            return await ctx.send(embed=embed)

        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            embed = nextcord.Embed(
                title="▶️ Play Music", description="📢 | Joining your voice channel...", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            msg = await ctx.send(embed=embed)
            vc: wavelink.Player = ctx.voice_client
            await vc.move_to(ctx.author.voice.channel)
            return msg
            await asyncio.sleep(7)
            msg.delete()

            
        else:
            vc: wavelink.Player = ctx.voice_client

        if vc.queue.is_empty and not vc.is_playing():

            view = MusicController()
            embed = nextcord.Embed(title="▶️ Playing Music..",
                                description=f"📢 | Now Playing `{search.title}` by {search.author} \n **LINK:** {search.uri}", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                            url=self.bot.user.display_avatar)
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
                            url=self.bot.user.display_avatar)
            embed.add_field(name="Duration",
                            value=humanfriendly.format_timespan(search.duration))
            msg = await ctx.send(embed=embed)
            await asyncio.sleep(5)
            await msg.delete()
  
        vc.ctx = ctx
        setattr(vc, "loop", False)

    @commands.command(name="pause", description="⏸️ Pauses playing song.")
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="⏸️ Pause Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        elif not ctx.author.voice:
            embed = nextcord.Embed(
                title="⏸️ Pause Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client

        embed = nextcord.Embed(title="⏸️ Pausing Music..",
                               description=f"📢 | ⏸️ Paused the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         url=self.bot.user.display_avatar)
        await vc.pause()
        message = await ctx.send(embed=embed, view=None)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="resume", description="⏯️ Resumes playing song.")
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="⏯️ Resume Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏯️ Resume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client

        embed = nextcord.Embed(title="⏸️ Resuming Music..",
                               description=f"📢 | ⏯️ Resumed the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         url=self.bot.user.display_avatar)
        await vc.resume()
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="loop", description="Enables Looping")
    async def loop(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="<:loop:950322712805507104> Loop Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="<:loop:950322712805507104> Loop Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client

        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)

        if vc.loop:
            return await ctx.send("Enabled <:loop:950322712805507104> Loop")        
        else:
            return await ctx.send("Disabled <:loop:950322712805507104> Loop")        
      

    @commands.command(name="queue", description="Queues a song..")
    async def queue(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="⏯️ Resume Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏯️ Resume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client    

        if vc.queue.is_empty:
            embed = nextcord.Embed(
                title="➕ Queue Music..", description=f"📢 | The queue is empty.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed, view=MessageDelete())
            await asyncio.sleep(7)
            await message.delete()    

        embed = nextcord.Embed(
                title="➕ Queue Music..", description=f"📢 | The queue is given below.", color=0x91cd0e)
        queue = vc.queue.copy()
        song_count = 0
        for song in queue:
            song_count +=1
            embed.add_field(name="‏‏‎ ", value=f"{song_count} - {song.title}", inline=False)

        await ctx.send(embed=embed, view=MessageDelete())    

    @commands.command(name="stop", description="⏸ Stops playing song.")
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="⏸ Stop Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()
        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="⏸ Stop Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client

        embed = nextcord.Embed(title="⏸ Stopping Music..",
                               description=f"📢 | ⏸️ Stoped the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         url=self.bot.user.display_avatar)
        await vc.stop()
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="vcdisconnect", description="🔌 Disconnects from the vc.")
    async def disconnect(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title="🔌 Disconnect Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="🔌 Disconnect Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client

        embed = nextcord.Embed(title="🔌 Disconnecting Music..",
                               description=f"📢 |🔌 Disconnected Successfully.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         url=self.bot.user.display_avatar)
        await vc.disconnect()
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="connect", description="🔌 Connects from the vc.")
    async def connect(self, ctx: commands.Context):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="🔌 Connect Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             url=self.bot.user.display_avatar)
            return await ctx.send(embed=embed)

        else:
            vc: wavelink.Player = ctx.voice_client

        embed = nextcord.Embed(title="🔌 Connecting Music..",
                               description=f"📢 |🔌 Connected Successfully.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility",
                         url=self.bot.user.display_avatar)
        await vc.connect(timeout=14, reconnect=True)
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()



    @commands.command(name="lyrics", description="Sends the lyrics of the song.")
    async def lyrics(self, ctx,*, name: str):
        url = f"https://some-random-api.ml/lyrics?title="
        player = wavelink.Player 
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
                    embed.set_author(name=data["author"], url=self.bot.user.display_avatar)
                    embed.set_thumbnail(url=data["thumbnail"]["genius"])  
                    await ctx.send(embed=embed, view=view) 

                except KeyError:
                    pass
                           

def setup(bot):
    bot.add_cog(Music(bot))
