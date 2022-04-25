import nextcord, asyncio
from typing import Optional, Union
from util.constants import Emojis

DELETE_BUTTON_EMOJI = Emojis.trashcan


# A new nextcord view
class DeleteMessage(nextcord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=None)
        self.ctx = ctx
        
    async def interaction_check(self, interaction):
        if interaction.user != self.ctx.author:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True
        
    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.secondary, emoji=DELETE_BUTTON_EMOJI)  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()  
        
class DeleteMessageWithNoChecks(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.secondary, emoji=DELETE_BUTTON_EMOJI)  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()  
        
class DeleteMessageSlash(nextcord.ui.View):
    def __init__(self, interaction):
        super().__init__(timeout=None)
        self.interaction = interaction
        
    async def interaction_check(self, interaction):
        if interaction.user != self.interaction.user:
            await interaction.response.send_message(":no_entry: This is not for you.", ephemeral=True)
            return False
        else:
            return True
    @nextcord.ui.button(label="Delete", style=nextcord.ButtonStyle.secondary, emoji=DELETE_BUTTON_EMOJI)  
    async def stop(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        await interaction.message.delete()  


class DeleteMessageAdvance(nextcord.ui.View):    
     """This should only be used on responses from interactions."""

     def __init__(self, user: Union[int, nextcord.User, nextcord.Member], *, timeout: float = 1, allow_manage_messages: bool = True, initial_message: Optional[Union[int, nextcord.Message]] = None,):
         if isinstance(user, (nextcord.User, nextcord.Member)):
            user = user.id   

         super().__init__(timeout=timeout)
         self.delete_button.custom_id = "message_delete_button"    
         permissions = nextcord.Permissions() 

         if allow_manage_messages:
             permissions.manage_messages = True
         self.delete_button.custom_id += str(permissions.value) + ":"
         self.delete_button.custom_id += str(user)

         self.delete_button.custom_id += ":"
         if initial_message:
            if isinstance(initial_message, nextcord.Message):
                initial_message = initial_message.id
            self.delete_button.custom_id += str(initial_message)

         @nextcord.ui.button(style=nextcord.ButtonStyle.grey, emoji=DELETE_BUTTON_EMOJI,)
         async def delete_button(self, button: nextcord.ui.Button, inter: nextcord.Interaction) -> None:
            """Delete a message when a button is pressed if the user is okay to delete it."""
            await asyncio.sleep(3)