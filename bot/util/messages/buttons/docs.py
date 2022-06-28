import nextcord
from nextcord.ext import commands

from util.constants import Emojis

class DocsView(nextcord.ui.View):
    
    def __init__(self, *, ctx: commands.Context=None, inter: nextcord.Interaction = None, key, url):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.inter = inter
        self.add_item(nextcord.ui.Button(label=key, style=nextcord.ButtonStyle.url, url=url, row=0))

    async def interaction_check(self, interaction):
        
        if not self.inter:
            user = self.ctx.author

        else:
            user = self.inter.user    

        if interaction.user != user:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True        
        
    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.secondary, emoji=Emojis.trashcan, row=1)  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()  