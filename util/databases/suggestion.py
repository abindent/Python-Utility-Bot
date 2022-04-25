import util
from util.mongo import Document





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
