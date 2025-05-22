import discord

# A new discord view
class DelBtnSlashInteractionCheck(discord.ui.View):
    def __init__(self, interaction: discord.Interaction):
        super().__init__(timeout=None)
        self.interaction = interaction
        
    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user != self.interaction.user:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True
    @discord.ui.button(label="Delete", style=discord.ButtonStyle.secondary, emoji="<:dustbin:949602736633167882>")  
    async def stop(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()  