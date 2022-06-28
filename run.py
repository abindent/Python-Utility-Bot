import subprocess

def run_bot():
   subprocess.check_call(["python", "bot/bot.py"])


if __name__ == "__main__":
    run_bot()

