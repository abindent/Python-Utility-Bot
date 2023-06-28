import subprocess

def run_bot_only():
     subprocess.check_call(["python", "bot/bot.py"])
     

if __name__ ==  "__main__":
    run_bot_only()
    
