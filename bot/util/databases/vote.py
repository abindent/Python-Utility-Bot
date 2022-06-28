import os, util
from util.mongo import Document

class VoteManage:
    def __init__(self, bot):
        self.db = bot.db
        self.vote_db = Document(self.db, "votes")
        self.user_db = Document(self.db, "users")
        print("Initialized Voting Database\n-----")
    
    # async def create_vote(self, dict):
    #     await self.vote_db.upsert(dict)

    async def add_like(self, _id):
        source = await self.vote_db.find_by_id(_id)

        likes = source["Likes"] 
        likes = likes + 1

        await self.vote_db.update_one({"_id": _id}, {'$set': {"Likes":likes}})

    async def add_dislike(self, _id):
        source = await self.vote_db.find_by_id(_id)

        dislikes = source["Dislikes"] 
        dislikes = dislikes + 1

        await self.vote_db.update_one({"_id": _id}, {'$set': {"Dislikes":dislikes}})

    async def get_data(self, _id):
        data = await self.vote_db.find_by_id(_id)
                
        Dislikes= data["Dislikes"] 
        Likes = data["Likes"]
        TotalVotes = Dislikes +  Likes

        data = {
            "Likes" : Likes,
            "Dislikes": Dislikes,
            "Total Votes" : TotalVotes,
        }

        return data

    async def add_user_data(self, dict):
         await self.user_db.upsert(dict)

    async def check_user_vote_status(self, user_id) -> bool:
        try:
            data = await self.user_db.find_by_id(user_id)
            
            voted = data["voted"]
            
            return True if voted is True else False

        except Exception as error:
            return False    