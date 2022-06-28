from util.mongo import Document


class InviteDB:
    def __init__(self, bot):
        self.invites = Document(bot.db, "invites")

    async def invite_data_existence_check(self, guild_id: int, inviter_id: int):
        data = await self.invites.find_by_custom({"guild_id": guild_id, "inviter_id": inviter_id})

        return data if data else None

    async def invite_data_existence_check_by_guild_id(self, guild_id: int):
        data = await self.invites.find_by_custom({"guild_id": guild_id})

        return data if data else None

    async def create_data(self, guild_id: int, inviter_id: int, data):
        await self.invites.upsert_custom(
            {"guild_id": guild_id, "inviter_id": inviter_id}, data
        )

    async def create_data_by_guild_id(self, guild_id: int, data):
        await self.invites.upsert_custom({"guild_id": guild_id}, data)    
