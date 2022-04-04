import nextcord

# A new nextcord view
class DelBtn(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        
    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True
        
    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.secondary, emoji="<:dustbin:949602736633167882>")  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()  
        
class DelBtnNoInteractionCheck(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.secondary, emoji="<:dustbin:949602736633167882>")  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()  
        
class DelBtnSlashInteractionCheck(nextcord.ui.View):
    def __init__(self, interaction):
        super().__init__(timeout=None)
        self.interaction = interaction
        
    async def interaction_check(self, interaction):
        if interaction.user != self.interaction.user:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True
    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.secondary, emoji="<:dustbin:949602736633167882>")  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()  