import nextcord, wavelink
from util.constants import Emojis

class DocsView(nextcord.ui.View):
    def __init__(self, ctx, key, url):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.add_item(nextcord.ui.Button(label=key, style=nextcord.ButtonStyle.url, url=url))

    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True        
        
    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.secondary, emoji=Emojis.trashcan)  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()  