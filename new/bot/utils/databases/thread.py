from utils.mongo import Document


class SupportDB:
    def __init__(self, bot):
        self.db = bot.db
        self.support_thread = Document(bot.db, "support_thread")

    async def get_data(self, guild_id):
        data = await self.support_thread.find_by_id(guild_id)
        return data

    async def create_table(self, guild_id, support_channel_id, log_channel_id):
        dict = {
            "_id": guild_id,
            "support_channel": support_channel_id,
            "log_channel": log_channel_id
        }

        try:
            await self.support_thread.upsert(dict)
            return True
        except Exception:
            return False

    async def delete_table(self, guild_id: int):

        await self.support_thread.delete_by_id(guild_id)
