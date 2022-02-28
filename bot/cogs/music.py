import nextcord, wavelink, os, asyncio, humanfriendly
from nextcord.ext import commands



class MusicController(nextcord.ui.View):
    def __init__(self):
         super().__init__()
 

    @nextcord.ui.button(label="Pause", style=nextcord.ButtonStyle.secondary, emoji="⏸️")  
    async def pause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
         embed=nextcord.Embed(title="⏸️ Pause Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
         embed.set_author(name="OpenSourceGames Utility", url=interaction.client.user.display_avatar)
         await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed=nextcord.Embed(title="⏸️ Pause Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility", url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client   

        embed=nextcord.Embed(title="⏸️ Pausing Music..", description=f"📢 | ⏸️ Paused the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility", url=interaction.client.user.display_avatar)
        await vc.pause()
        await interaction.response.send_message(embed=embed, ephemeral=True)
        

    @nextcord.ui.button(label="Resume", style=nextcord.ButtonStyle.secondary, emoji="⏯️")
    async def resume(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
          embed=nextcord.Embed(title="⏯️ Resume Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
          embed.set_author(name="OpenSourceGames Utility", url=interaction.client.user.display_avatar)
          await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed=nextcord.Embed(title="⏯️ Resume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility", url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        else:
            vc: wavelink.Player = interaction.guild.voice_client   

        embed=nextcord.Embed(title="⏯️ Resuming Music..", description=f"📢 |⏯️ Resumed the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility", url=interaction.client.user.display_avatar)
        await vc.resume() 
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @nextcord.ui.button(label="Stop", style=nextcord.ButtonStyle.secondary, emoji="⏹️")  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.guild.voice_client:
            embed=nextcord.Embed(title="⏸ Stop Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility", url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)

        elif not getattr(interaction.user.voice, "channel", None):
            embed=nextcord.Embed(title="⏸ Stop Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility", url=interaction.client.user.display_avatar)
            await interaction.response.send_message(embed=embed, ephemeral=True)


        else:
            vc: wavelink.Player = interaction.guild.voice_client
 
        for child in self.children: 
            child.disabled = True 
            await interaction.message.edit(view=self)  
        await vc.disconnect()
        await interaction.response.send_message(f"{interaction.user.mention} we have closed the interaction.", ephemeral=True) 
        
        



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

    @commands.command(name="play", description="▶️ Plays a song for you that you want.")
    async def play(self, ctx: commands.Context, *,search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            
        elif not getattr(ctx.author.voice, "channel", None):
            embed=nextcord.Embed(title="▶️ Play Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
            message =  await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client  
            
            
        view = MusicController()                      
        embed=nextcord.Embed(title="▶️ Playing Music..", description=f"📢 | Now Playing `{search.title}` by {search.author} \n **LINK:** {search.uri}", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
        embed.add_field(name="Duration", value=humanfriendly.format_timespan(search.duration))
        embed.set_image(url=search.thumbnail)
        await vc.play(search)
        await ctx.send(embed=embed, view=view)      

    @commands.command(name="pause", description="⏸️ Pauses playing song.")   
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
         embed=nextcord.Embed(title="⏸️ Pause Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
         embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
         message = await ctx.send(embed=embed)
         return message
         await asyncio.sleep(5)
         await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed=nextcord.Embed(title="⏸️ Pause Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
            message =  await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client   

        embed=nextcord.Embed(title="⏸️ Pausing Music..", description=f"📢 | ⏸️ Paused the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
        await vc.pause() 
        message = await ctx.send(embed=embed,view=None)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="resume", description="⏯️ Resumes playing song.")   
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
         embed=nextcord.Embed(title="⏯️ Resume Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
         embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
         message = await ctx.send(embed=embed)
         return message
         await asyncio.sleep(5)
         await message.delete()

        elif not getattr(ctx.author.voice, "channel", None):
            embed=nextcord.Embed(title="⏯️ Resume Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else: 
            vc: wavelink.Player = ctx.voice_client   

        embed=nextcord.Embed(title="⏸️ Resuming Music..", description=f"📢 | ⏯️ Resumed the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
        await vc.resume() 
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    # @commands.command(name="nowplaying", aliases=["np"], description="Returns the song playing currently")
    # async def get_now_playing(self, ctx: commands.Context):
    #   s


    @commands.command(name="stop", description="⏸ Stops playing song.")   
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
         embed=nextcord.Embed(title="⏸ Stop Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
         embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
         message = await ctx.send(embed=embed)
         return message
         await asyncio.sleep(5)
         await message.delete()
        elif not getattr(ctx.author.voice, "channel", None):
            embed=nextcord.Embed(title="⏸ Stop Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client   

        embed=nextcord.Embed(title="⏸ Stopping Music..", description=f"📢 | ⏸️ Stoped the player.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
        await vc.stop() 
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    @commands.command(name="vcdisconnect", description="🔌 Disconnects from the vc.")   
    async def disconnect(self, ctx: commands.Context):
        if not ctx.voice_client:
         embed=nextcord.Embed(title="🔌 Disconnect Music..", description=f"📢 | Your are not playing a song.", color=0x91cd0e)
         embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
         message = await ctx.send(embed=embed)
         return  message
         await asyncio.sleep(5)
         await message.delete() 

        elif not getattr(ctx.author.voice, "channel", None):
            embed=nextcord.Embed(title="🔌 Disconnect Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
            message = await ctx.send(embed=embed)
            return  message
            await asyncio.sleep(5)
            await message.delete()

        else:
            vc: wavelink.Player = ctx.voice_client   

        embed=nextcord.Embed(title="🔌 Disconnecting Music..", description=f"📢 |🔌 Disconnected Successfully.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
        await vc.disconnect() 
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await  message.delete()

    @commands.command(name="connect", description="🔌 Connects from the vc.")   
    async def connect(self, ctx: commands.Context):
        if not ctx.voice_client:
          vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)

        elif not getattr(ctx.author.voice, "channel", None):
            embed=nextcord.Embed(title="🔌 Connect Music", description="📢 | Join a voice channel please.", color=0x91cd0e)
            embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
            return await ctx.send(embed=embed)

        else:
            vc: wavelink.Player = ctx.voice_client   

        embed=nextcord.Embed(title="🔌 Connecting Music..", description=f"📢 |🔌 Connected Successfully.", color=0x91cd0e)
        embed.set_author(name="OpenSourceGames Utility", url=self.bot.user.display_avatar)
        await vc.connect(timeout=14, reconnect=True) 
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await  message.delete()
    



def setup(bot):
    bot.add_cog(Music(bot))        
