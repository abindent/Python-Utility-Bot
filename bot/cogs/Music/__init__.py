import nextcord, json, wavelink, os, asyncio, humanfriendly, aiohttp, datetime
from nextcord.ext import commands
from util.messages import DeleteMessage as MessageDelete
from util.messages.buttons.music import MusicController

        
class Music(commands.Cog, description="Listen and Control that music which you want."):

    COG_EMOJI = "🎶"
    
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.node_connect())

    async def node_connect(self):
        await self.bot.wait_until_ready()
        await wavelink.NodePool.create_node(bot=self.bot, host="lavalink-replit.thinkwithus.repl.co", port=443, password="SleepingOnTrains", https=True)


    @commands.Cog.listener()
    async def on_waveink_node_ready(self, node: wavelink.Node):
        print(f"Node <{node.id}> is ready!")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        ctx = player.ctx
        vc: player = ctx.voice_client

        if vc.loop:
            return await vc.stop(), await vc.play(track), await songplayembed.edit(view=MusicController(self._global_ctx))

        if vc.queue.is_empty:
            return await vc.stop(), await songplayembed.edit(view=MessageDelete(self._global_ctx))
              

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


    @commands.command(name="play", description="Plays a song for you that you want.", usage="<song name>")
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)

        elif not ctx.author.voice:
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            return await ctx.send(embed=embed)
            return msg, await asyncio.sleep(7), msg.delete()

        elif not ctx.author.voice.channel == ctx.me.voice.channel:
            embed = nextcord.Embed(
                title=f"📢 | Joining your voice channel...", color=0x91cd0e)
            msg = await ctx.send(embed=embed)
            vc: wavelink.Player = ctx.voice_client
            await vc.move_to(ctx.author.voice.channel)
            return msg, await asyncio.sleep(7), msg.delete()

            
        else:
            vc: wavelink.Player = ctx.voice_client

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

    @commands.command(name="pause", description="Pauses playing song.")
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        elif not ctx.author.voice:
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client

        if ctx.author is self._global_ctx.author:
            embed = nextcord.Embed(title=f"📢 | ⏸️ Paused the player.", color=0x91cd0e)
            await vc.pause()
            message = await ctx.send(embed=embed, view=None)
            await asyncio.sleep(5)
            await message.delete()
        
        else:
            msg = await ctx.send(":no_entry: This song is not yours, so you can't pause it.")
            await asyncio.sleep(5)
            await msg.delete         

    @commands.command(name="resume", description="Resumes playing song.")
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client
          
        if ctx.author is self._global_ctx.author:  
           embed = nextcord.Embed(title=f"📢 | ⏯️ Resumed the player.", color=0x91cd0e)
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
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5),await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client
     
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
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility",
                             icon_url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message,await asyncio.sleep(5),await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client    

        if vc.queue.is_empty:
            embed = nextcord.Embed(
                title=f"📢 | The queue is empty.", color=0x91cd0e)
            message = await ctx.send(embed=embed, view=MessageDelete())
            await asyncio.sleep(7)
            await message.delete()    

        embed = nextcord.Embed(
                title=f"📢 | The queue is given below.", color=0x91cd0e)
        queue = vc.queue.copy()
        song_count = 0
        for song in queue:
            song_count +=1
            embed.add_field(name="‏‏‎ ", value=f"**{song_count})** {song.title}", inline=False)

        await ctx.send(embed=embed, view=MessageDelete())    

    @commands.command(name="stop", description="Stops playing song.")
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="📢 | Join a voice channel please.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client

        embed = nextcord.Embed(title=f"📢 | ⏸️ Stoped the player.", color=0x91cd0e)
        await vc.stop()
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="disconnect", aliases=["vcdisconnect"], description="🔌 Disconnects from the vc.")
    async def vcdisconnect(self, ctx: commands.Context):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | Your are not playing a song.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed = nextcord.Embed(
                title="📢 | Join a voice channel please.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client

        embed = nextcord.Embed(title=f"📢 |🔌 Disconnected Successfully.", color=0x91cd0e)
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
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(5), await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client

        embed = nextcord.Embed(title=f"📢 |🔌 Connected Successfully.", color=0x91cd0e)
        await vc.connect(timeout=14, reconnect=True)
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="volume", aliases=["setvolume", "changevolume"], description="Sets the volume of the player.")
    async def setvolume(self, ctx: commands.Context, *, volume: int):
        if not ctx.voice_client:
            embed = nextcord.Embed(
                title=f"📢 | I am not in a voice channel.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(4), message.delete()

        elif not ctx.author.voice:
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(4), message.delete()

            
        else:
            vc: wavelink.Player = ctx.voice_client
        
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
                title=f"📢 | I am not in a voice channel.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(4), message.delete()

        elif not ctx.author.voice:
            embed = nextcord.Embed(
                title=f"📢 | Join a voice channel please.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(4), message.delete()

            
        else:
            vc: wavelink.Player = ctx.voice_client

        if not vc.is_playing():
            embed = nextcord.Embed(
                title=f"📢 | You are not even playing a music.", color=0x91cd0e)
            message = await ctx.send(embed=embed)
            return message, await asyncio.sleep(4), message.delete()

        embed = nextcord.Embed(title=f"🎶 | I am playing `{vc.track.title}` by {vc.track.author} \n **VIDEO LINK:** {vc.track.uri}", color=0x91cd0e)
        embed.add_field(name="Duration",
                        value=humanfriendly.format_timespan(vc.track.length))
        embed.set_image(url=vc.track.thumbnail)
        await ctx.send(embed=embed, view=MessageDelete())    



    @commands.command(name="lyrics", description="Sends the lyrics of the song.", usage="<song name>")
    async def lyrics(self, ctx,*, name: str):
        url = "https://some-random-api.ml/lyrics?title="
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

                    view = MessageDelete(ctx)
                    embed = nextcord.Embed(title=data["title"], description=data["lyrics"], color=nextcord.Color.blue(), timestamp=datetime.datetime.utcnow()) 
                    embed.set_author(name=data["author"], icon_url=self.bot.user.display_avatar)
                    embed.set_thumbnail(url=data["thumbnail"]["genius"])  
                    await ctx.send(embed=embed, view=view) 

                except KeyError:
                    pass
                           
