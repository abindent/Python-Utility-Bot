from utils.mongo import Document


class Blacklist_DB:
    def __init__(self, bot):
        self.db = bot.db
        self.blacklisted_users = Document(bot.db, "blacklisted_users")

    async def get_data(self, user_id):
        data = await self.blacklisted_users.find_by_id(user_id)
        return data

    async def create_user_table(self, guild_id, user):
        dict = {
            "_id": user.id,
            "guild_id": guild_id,
            "user_name": user.name
        }
        await self.blacklisted_users.upsert(dict)

    async def delete_user_table(self, user_id):

        await self.blacklisted_users.delete_by_id(user_id)

    async def check_user_blacklisted_status(self, user_id, guild_id) -> bool:

        data = await self.blacklisted_users.find_by_id(user_id)
        d=await self.blacklisted_users.get_all()
        for c in d:
            print(d) 
        return True if data else False
