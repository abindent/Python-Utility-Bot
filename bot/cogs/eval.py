import nextcord, asyncio, os, io, contextlib
from nextcord.ext import commands


class DelBtn(nextcord.ui.View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.secondary, emoji="\N{WASTEBASKET}")  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()
        
class Eval(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
      
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")  
        
        
    @commands.command(name="excecute", description="Evaluates the given python code", aliases=['eval', 'exec', 'evaluate'])
    async def excecute(self, ctx: commands.Context, *, code):
           view = DelBtn()
           stdout = io.StringIO()
           with contextlib.redirect_stdout(stdout):
                 exec(code) 
           output =  stdout.getvalue()
           TOKEN = self.bot.config_token
           if ouput is TOKEN :
                output = "None" 
                
           embed = nextcord.Embed(title="Your code", description="✅ Your eval job has been completed and the result is provided below.", color=0x00FF00)
           embed.add_field(name="Input Code", value=f"```py\n{code}\n```", inline=False)
           embed.add_field(name="Evaluated Code", value=output, inline=False)     
           await ctx.send(embed=embed, view=view) 
  
        
def setup(bot):
    bot.add_cog(Eval(bot))                         
