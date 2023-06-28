import subprocess

def install():
    subprocess.check_call(["python", "install_packages.py"])
     
def run():     
    subprocess.check_call(["python", "bot/bot.py"])
  
def run_bot():
     install()
     run()     

if __name__ ==  "__main__":
    run_bot()
    
