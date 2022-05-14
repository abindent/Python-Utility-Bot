# 🤖 Nextcord Bot Template
A simple template for building a beautiful discord bot with nextcord.Here I have also implemented the buttons, discord modals and select menus along with slash commands. This project is under progress so you have to wait for some time to get your wanted features.

## 💻 Features 
1. Added MongoDB databse for saving bot data (eg:- bot prefix).
2. Added Listeners and added a lot of bot customization options.
3. Dynamic help command with buttons.
4. Added sub-commands examples in `__sub-command.py`.
5. Added some commands related to the stats of the bot.
6. Added some commands to send channel stats, to create or delete channels.
7. Added a cog handler.
8. Added configuration cog.
9. Added ping and eval command.
10. Added fun commands.
11. Added music cog.
12. Added utility cog.
13. Added suggestion cog.
14. Added slash commands. 
15. Added discord modals.

## 💻 How to setup
### Step 1
 Run ```git clone https://github.com/abindent/Nextcord-Utility-Bot.git``` this command to our terminal for cloning this repo.
 
### Step 2
 Add environment variable file (eg:- `.env`, `.env.local`, `.env.developement`).
 
 
 After creating a .env file add the following lines
     
        BOT_TOKEN=<Your bot's token>
        MONGO_URI=<connection string to your mongodb collection>
        JOKE_API=<rapidapi key>
        secret_id=<random hard to guess string>    
        ALGOLIA_SEARCH_APP_ID=BH4D9OD16A
        ALGOLIA_SEARCH_API_KEY=f37d91bd900bbb124c8210cca9efcc01
 

### Step 3
 Install dependencies using ```pip install -r requirements.txt``` and run `python bot/bot.py` in your local machine.


## 📝 Task list
- [x] To add custom prefix.
- [x] To add eval command.
- [x] To add games and activity commands in bot. 
- [ ] To format code and enhance it.
- [x] To add new discord modal here.

## Main Dependencies 
1) **NEXTCORD** 
 
     ![PyPI](https://img.shields.io/pypi/v/nextcord?style=for-the-badge)

2) **NEXTCORD-EXT-MENUS**
 
    ![PyPI](https://img.shields.io/pypi/v/nextcord-ext-menus?style=for-the-badge)

3) **NEXTCORD-EXT-IPC**
 
    ![PyPI](https://img.shields.io/pypi/v/nextcord-ext-ipc?style=for-the-badge)

4) **PYMONGO**

    ![PyPI](https://img.shields.io/pypi/v/PyMongo?style=for-the-badge)

5) **MOTOR**

    ![PyPI](https://img.shields.io/pypi/v/motor?style=for-the-badge)

6) **HUMANFRIENDLY**

    ![PyPI](https://img.shields.io/pypi/v/humanfriendly?style=for-the-badge)

7) **NEXTWAVE**

    ![PyPI](https://img.shields.io/pypi/v/nextwave?style=for-the-badge)
