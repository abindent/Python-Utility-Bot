import os,json, pymongo
from utils.mongo import *


class PollSetup:
     def __init__(self, bot):
         super().__init__()
         try:
             poll_db = bot.poll_db
             self.poll_db = Document(poll_db, "poll")
             self.poll_votes_db = Document(poll_db, "poll_votes")
             print("Initialized Database for poll")
         except Exception as error:
             print(error)

     def create_poll(self, vote: int, time: int, message_id: int):
        try:
           poll_data = {
               "_id" : message_id,
               "poll" : f"{vote}",
               "Time" : f"{time}",
            }

           self.poll_db.upsert(poll_data)   
        
        except Exception as error:
            print(error)

     def create_user_data(self, user_id, message_id: int, voted: bool):
         try:
           user_data = {
               "_id": user.id,
               "message_id": message_id,
               "voted": voted,
           } 
           self.poll_votes_db.upsert(user_data)

         except Exception as error:
             print(error)

     def get_poll_data(self, _id):
         try:
            data = self.poll_db.get_by_id(_id)
            user_data =  json.load(data)

            return user_data
            
         except Exception as error:
             print(error)   

     def get_user_data(self, _id):
         try:
            data = self.poll_votes_db.get_by_id(_id)
            user_data =  json.load(data)

            return user_data
            
         except Exception as error:
             print(error)    

     def check_user_vote(self, user_id, message_id) -> bool:
         try:
           poll_data = self.get_poll_data(message_id)

           poll_id = poll_data["_id"]
 
           user_data = self.get_user_data(user_id)

           user_message_id = user_data["message_id"]
            
           return True if poll_id is user_message_id else False

         except:
            return False   
              

     def delete_poll(self, user_id, message_id):
         try:
             self.poll_db.delete(message_id)
             self.poll_votes_db.delete(user_id)

         except Exception as error:
              print(error)



      




            


            
           

            

            

   