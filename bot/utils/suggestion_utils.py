import nextcord
from nextcord.ext import application_checks
from utils.mongo import Document


class MakeSuggesstionLink(nextcord.ui.View):
    def __init__(self, guild_id, channel_id, suggesion_id):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Link to the embed", style=nextcord.ButtonStyle.url,
                      url=f"https://discord.com/channels/{guild_id}/{channel_id}/{suggesion_id}"))


class SuggestionBtn(nextcord.ui.View):
    def __init__(self, db):
        super().__init__(timeout=600000)
        self.db = db

    @nextcord.ui.button(label="Approve Now", style=nextcord.ButtonStyle.secondary, emoji="✅")
    @application_checks.has_guild_permissions(manage_messages=True, create_public_threads=True, send_messages_in_threads=True)
    async def _approve_btn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        data = await self.db.get_data(interaction.guild.id)

        if not data:
            suggestion_channel = await interaction.guild.create_text_channel('📨｜suggestions')
            approve_channel = await interaction.guild.create_text_channel('✔｜approved-suggestions')
            deny_channel = await interaction.guild.create_text_channel('❌｜denied-suggestions')

            await self.db.add_data(interaction.guild.id, suggestion_channel.id, approve_channel.id, deny_channel.id)
            data = await self.db.get_data(ctx.guild.id)
            suggestion_channel = interaction.client.get_channel(data["channel_id"])
            channel = interaction.client.get_channel(data["approve_channel_id"])
        try:
         suggestion_channel = interaction.client.get_channel(data["channel_id"])
         channel = interaction.client.get_channel(data["approve_channel_id"])

        except:
            await interaction.response.send_message(":no_entry: Please set all the channels manually for using the suggestion system. For more run `[prefix]help setup channel`", ephemeral=True)

        suggestion_msg = await suggestion_channel.fetch_message(interaction.message.id)
        if not await self.db.check_approved(interaction.message.id):
            await self.db.update_review(suggestion_msg.id, isReviewed="accepted")
            suggestion_data = await self.db.get_message_data(interaction.message.id)
            suggestion_body = suggestion_data["suggestion"]
            sno = suggestion_data["serial_no"]
            suggested_by = interaction.client.get_user(suggestion_data["suggestor_id"])

            embed = nextcord.Embed(
                title=f'✅ Suggestion #{sno} has been approved by {interaction.user}.', color=nextcord.Color.green())
            embed.set_author(
                name=f'{suggested_by.name}#{suggested_by.discriminator}', icon_url=suggested_by.display_avatar)
            embed.add_field(
                name="Suggestion", value=f'{suggestion_body}\n\n')
            embed.add_field(
                name="Reason", value="*Instant Apporval [No Reason is nedded for an instant approval.]*", inline=False)
            embed.set_footer(
                text=f"Auhtor ID: {suggestion_data['suggestor_id']}")
            
            await channel.send(embed=embed, view=MakeSuggesstionLink(interaction.guild.id, suggestion_channel.id, suggestion_msg.id))
            
            self._approve_btn.label = "Approved"
            self._approve_btn.disabled = True
            self.remove_item(self._deny_btn)
            await interaction.message.edit(view=self)
            
            
        else:
            data = await self.db.get_message_data(suggestion_msg.id)

            await interaction.response.send_message(f"Someone has already {data['isReviewed']} this suggestion.", ephemeral=True)
            await interaction.message.edit(view=None)

    @nextcord.ui.button(label="Deny Now", style=nextcord.ButtonStyle.secondary, emoji="❌")
    @application_checks.has_guild_permissions(manage_messages=True, create_public_threads=True, send_messages_in_threads=True)
    async def _deny_btn(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        data = await self.db.get_data(interaction.guild.id)

        if not data:
            suggestion_channel = await interaction.guild.create_text_channel('📨｜suggestions')
            approve_channel = await interaction.guild.create_text_channel('✔｜approved-suggestions')
            deny_channel = await interaction.guild.create_text_channel('❌｜denied-suggestions')

            await self.db.add_data(interaction.guild.id, suggestion_channel.id, approve_channel.id, deny_channel.id)
            data = await self.db.get_data(ctx.guild.id)
            suggestion_channel = interaction.client.get_channel(data["channel_id"])
            channel = interaction.client.get_channel(data["deny_channel_id"])
        
        suggestion_channel = interaction.client.get_channel(data["channel_id"])
        channel = interaction.client.get_channel(data["deny_channel_id"])

        
           
        suggestion_msg = await suggestion_channel.fetch_message(interaction.message.id)

        if not await self.db.check_approved(interaction.message.id):
            await self.db.update_review(suggestion_msg.id, isReviewed="rejected")
            suggestion_data = await self.db.get_message_data(interaction.message.id)
            suggestion_body = suggestion_data["suggestion"]
            sno = suggestion_data["serial_no"]
            suggested_by = interaction.client.get_user(suggestion_data["suggestor_id"])

            embed = nextcord.Embed(
                title=f'❌ Suggestion #{sno} has been denied by {interaction.client.user}.', color=nextcord.Color.red())
            embed.set_author(
                name=f'{suggested_by.name}#{suggested_by.discriminator}', icon_url=suggested_by.display_avatar)
            embed.add_field(
                name="Suggestion", value=f'{suggestion_body}\n\n')
            embed.add_field(
                name="Reason", value="*Instant Denial [No Reason is needed for an instant denial.]*", inline=False)
            embed.set_footer(
                text=f"Auhtor ID: {suggestion_data['suggestor_id']}")
            
             
            await channel.send(embed=embed, view=MakeSuggesstionLink(interaction.guild.id, suggestion_channel.id, suggestion_msg.id))

            self._deny_btn.label = "Denied"
            self._deny_btn.disabled = True
            self.remove_item(self._approve_btn)
            await interaction.message.edit(view=self)
               
           
                
            
        else:
            data = await self.db.get_message_data(suggestion_msg.id)

            await interaction.response.send_message(f"Someone has already {data['isReviewed']} this suggestion.", ephemeral=True)
            
            await interaction.message.edit(view=None)
                

    async def on_timeout(self, interaction: nextcord.Interaction):
        await interaction.message.edit(view=None)


class SuggestionDB:
    def __init__(self, bot):
        self.db = bot.db
        self.suggestion_db = Document(self.db, "suggestion_db")
        self.suggestion_status_db = Document(self.db, "suggestion_status_db")

 # <!-- METHODS FOR ADDING DATA -->
    async def add_data(self, guild_id, channel_id=None, approve_channel_id=None, deny_channel_id=None):
        dict = {
            "_id": guild_id,
            "channel_id": channel_id,
            "approve_channel_id": approve_channel_id,
            'deny_channel_id': deny_channel_id,
            "suggestion_count": 1,
        }
        await self.suggestion_db.upsert(dict)

    async def create_message_data(self, message_id, user_id, sno, suggestion):
        dict = {
            "_id": message_id,
            "suggestor_id": user_id,
            "serial_no": sno,
            "suggestion": suggestion,
            "isReviewed": None,
        }
        await self.suggestion_status_db.upsert(dict)

    async def add_suggestion_count(self, guild_id):
        data = await self.suggestion_db.find_by_id(guild_id)
        data["suggestion_count"] += 1

        await self.suggestion_db.upsert(data)

 # <!-- METHODS TO ADD DATA -->
    async def get_message_data(self, message_id):
        data = await self.suggestion_status_db.find_by_id(message_id)
        return data

    async def get_data(self, guild_id):
        data = await self.suggestion_db.find_by_id(guild_id)
        return data

 # <!--  METHODS TO UPDATE DATA -->

    async def update_channel(self, guild_id, channel_id):
        data = await self.suggestion_db.find_by_id(guild_id)
        data["channel_id"] = channel_id

        await self.suggestion_db.upsert(data)

    async def update_approve_channel(self, guild_id, approve_channel_id):
        data = await self.suggestion_db.find_by_id(guild_id)
        data["approve_channel_id"] = approve_channel_id

        await self.suggestion_db.upsert(data)

    async def update_deny_channel(self, guild_id, deny_channel_id):
        data = await self.suggestion_db.find_by_id(guild_id)
        data["deny_channel_id"] = deny_channel_id
        await self.suggestion_db.upsert(data)

    async def update_review(self, message_id, isReviewed):
        data = await self.suggestion_status_db.find_by_id(message_id)
        data["isReviewed"] = isReviewed

        await self.suggestion_status_db.upsert(data)

 # <!-- Checking Suggestion Review Status -->
    async def check_approved(self, message_id) -> bool:
        data = await self.suggestion_status_db.find_by_id(message_id)

        if data["isReviewed"] == "accepted" or data["isReviewed"] == "rejected":
            return True
        else:
            return False
