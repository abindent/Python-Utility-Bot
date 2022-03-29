import nextcord, json, datetime
from nextcord.ext import commands, tasks
from utils.json import get_path, read_json, write_json


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = ['1\u20e3', '2\u20e3',
                      '3\u20e3', '4\u20e3',
                      '5\u20e3', '6\u20e3',
                      '7\u20e3', '8\u20e3',
                      '9\u20e3', '\U00001F51F']
    
    
 
def setup(bot):
    bot.add_cog(Poll(bot))