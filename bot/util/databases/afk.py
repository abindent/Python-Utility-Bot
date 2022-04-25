import nextcord
from util.mongo import Document

class afk_utils:
    def __init__(self, bot):
        self.db = bot.db
        self.afk_db = Document(self.db, "afk_user_db")
    
    
    async def create_afk(self, user, guild_id, reason):
        dict = {
            "_id" : user.id,
            "guild_id" : guild_id,
            "name" : user.name,
            "reason": reason
        }    
        
        await self.afk_db.upsert(dict)
    
    async def fetch_afk(self, id):
        data = await self.afk_db.find_by_id(id)
        
        return data

    async def delete_afk(self, id):
        await self.afk_db.delete_by_id(id)