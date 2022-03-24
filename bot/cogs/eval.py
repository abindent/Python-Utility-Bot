import nextcord, asyncio, os, io, contextlib
from nextcord.ext import commands
from nextcord.ui import Modal, TextInput

class DelBtn(nextcord.ui.View):


    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.secondary, emoji="<:dustbin:949602736633167882>")  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()

class SnekBox_Eval(nextcord.ui.Modal):
    def __init__(self) -> None:
     super().__init__(title="Evaluate Your Code", custom_id="evaluate_code")
     self.add_item(
            nextcord.ui.TextInput(
                label="Your Eval Code",
                placeholder="print('Hello')",
                custom_id="evaluated code",
                style=nextcord.TextInputStyle.paragraph,
                min_length=3
            ),
     )

    async def callback(self, inter: nextcord.Interaction) -> None:
        view = DelBtn()
        embed = nextcord.Embed(title="Your code", description="✅ Your eval job has been completed and the result is provided below.", color=0x00FF00)
        code = self.children[0].value
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
          exec(code)

        res = stdout.getvalue()
   
        if inter.client.config_token in res:
            res = ":warning: We can't reveal any sensitive info."

        embed.add_field(name="Input Code", value=f"```py\n{code}\n```", inline=False)
        embed.add_field(name="Evaluated Code:", value=res, inline=False)
        await inter.response.send_message(embed=embed,view=view)

    async def on_error(self, error, interaction: nextcord.Interaction):
        view = DelBtn()
        embed = nextcord.Embed(title="Code Status", description=":x: An error occurred.", color=0xFF0000)
        embed.add_field(name=":warning: The Error", value=f"```{error}```", inline=False)
        await interaction.response.send_message(embed=embed,view=view)

class Eval(commands.Cog):

    
    COG_EMOJI = "💻"

    def __init__(self, bot):
        self.bot = bot
        
      
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} Cog has been loaded\n-----")  
        
        
    @nextcord.slash_command(name="eval", description="Evaluates the given python code")
    async def eval(self, interaction: nextcord.Interaction):
        await interaction.response.send_modal(modal=SnekBox_Eval())
  
        
def setup(bot):
    bot.add_cog(Eval(bot))                         
