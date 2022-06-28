import re, time, datetime

from nextcord.ext import commands

class HumanfriendlyTime():
    def __init__(self, argument):
   
     self.argument = argument.lower()
     
     
     self.time_regex = re.compile(r"(?:(\d{1,5})(h|s|m|d))+?")
     self.time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}


    
    def set_type(self, __type) -> None:
       self.type = __type
       

    def get_ending_time(self, seconds):
                now = time.time()
                ts_epoch = now + seconds
                ts = datetime.datetime.fromtimestamp(ts_epoch).strftime('%Y-%m-%d %H:%M:%S')

                return ts

    def get_total_seconds(self, seconds):
                now = time.time()
                ts_epoch = now + seconds

                return round(ts_epoch)


    def get_creation_time_in_seconds(self):
        
               return round(time.time())         

    def convert(self, argument):
            args = argument.lower()
            matches = re.findall(self.time_regex, args)
            __time = 0
            for key, value in matches:
                try:
                    __time += self.time_dict[value] * float(key)
                except KeyError:
                    raise commands.BadArgument(
                        f"{value} is an invalid time key! h|m|s|d are valid arguments"
                    )
                except ValueError:
                    raise commands.BadArgument(f"{key} is not a number!")
            return round(__time)

    async def get_result(self, __type: str=None) -> None:
    
        self.set_type(__type)

        __evaluated_seconds = self.convert(self.argument)

        if self.type.__contains__("Total Seconds"):
            self.result = self.get_total_seconds(__evaluated_seconds)
          

        elif self.type.__contains__("Ending Time"):
            self.result = self.get_ending_time(__evaluated_seconds)

        elif self.type.__contains__("Creation Time"):
            self.result = self.get_creation_time_in_seconds()    

        else:
            if self.type is None:
                raise Exception("Please provide a type.")    
            else:
                raise Exception("The provided type is not valid. It must be either | Total Seconds | or | Ending Time | ")    

        return self.result        