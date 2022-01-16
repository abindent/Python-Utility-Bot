import asyncio
import aiohttp
import datetime
from io import BytesIO
import humanfriendly
import json
import nextcord
from nextcord.ext import commands, menus
import os
import random
from server import keep_alive
import urllib

def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]    

activity = nextcord.Activity(type=nextcord.ActivityType.watching,name="10/10 Shards")
client = commands.AutoShardedBot(
    command_prefix=get_prefix, shard_count=10, help_command=None, activity=activity, status=nextcord.Status.do_not_disturb)

# EVENTS
@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord.")
    
@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)]   = "t!"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

# CHANGE PREFIX COMMAND
@client.command(name="prefix", aliases=["setprefix"], description="Sets guild's prefix for the bot.")
async def prefix(ctx, setprefix=None):
    if(not ctx.author.guild_permissions.manage_channels):
        await ctx.send('This command requires ``Manage Messages`` permission.')
        return 

    if setprefix is None:
        setprefix = "t!"

    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = setprefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f"The prefix has changed to {setprefix}")    
# COMMAND LIST

# PING COMMAND
@client.command(name="ping", description="Returns the latency of the bot", aliases=["latency", "p", "pingpong"])
async def ping(ctx):
    await ctx.send(f"Pong! Latency is {round(client.latency)}ws")


# EIGHTBALL COMMAD
@client.command(name="eightball", aliases=["8ball", "8b"], description="Let the 8 Ball Predict!\n")
async def eightball(ctx, *, question):
    responses = [
        'It is certain.',
        'It is decidedly so.',
        'Without a doubt.',
        'Yes - definitely.',
        'You may rely on it.',
        'As I see it yes.',
        'Most likely.',
        'Outlook good.',
        'Yes.',
        'Signs point to yes.',
        'Reply hazy, try again.',
        'Better not tell you now.',
        'Concentrate and ask again.',
        "Don't count on it.",
        'I cannot predict now.',
        'My reply is no.',
        'My sources say no.',
        'Outlook not so good.',
        'VEry doubtfull.',
        'I am tired. *proceeds with sleeping*',
        'As I see it, yes.',
        'Yes.',
        'Positive',
        'From my point of view, yes',
        'Convinced.',
        'Most Likley.',
        'Chances High',
        'No.',
        'Negative.',
        'Not Convinced.',
        'Perhaps.',
        'Not Sure',
        'Mayby',
        'Im to lazy to predict.'
    ]
    await ctx.send(f":8ball: Question: {question}\n:8ball: Answer: {random.choice(responses)}")

# TOGGLE COMMANDS COMMAND
@client.command(name="toggle", aliases=["togglecmd", "editcmd"], description="Enables a Disabled Command and Disables an Enabled Command.")
@commands.has_guild_permissions(administrator=True)
async def toggle(ctx, *, command):
    command = client.get_command(command)

    if command == None:
        await ctx.send(f"**Requested command 😞 {command.name} not found.**")
    elif ctx.command == command:
        await ctx.send(f"{command.name} cannot be disabled.")
    else:
        command.enabled = not command.enabled
        ternary = "enabled" if command.enabled else "disabled"
        togglembed = nextcord.Embed(
            title=f"Toggled {command.qualified_name}", description=f"**The {command.qualified_name} command has been {ternary}**")
        togglembed.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        togglembed.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=togglembed)

# MEME COMMAND
@client.command(name="meme", description="Replies with a meme.")
async def meme(ctx):
    memeApi = urllib.request.urlopen("https://meme-api.herokuapp.com/gimme")
    memeData = json.load(memeApi)

    memeUrl = memeData["url"]
    memeName = memeData["title"]
    memePoster = memeData["author"]
    memeReddit = memeData["subreddit"]
    memeLink = memeData["postLink"]

    memeEmbed = nextcord.Embed(title=memeName, color=0x14cccc)
    memeEmbed.set_image(url=memeUrl)
    memeEmbed.set_footer(
        text=f"Meme by: {memePoster} | Subreddit: {memeReddit} | Post: {memeLink}")
    await ctx.send(embed=memeEmbed)


# EMOJI STEAL COMMAND
@client.command(name="emoji", aliases=["eadd"], description="Adds an external img (through the link of the img provided) as gif in your server.")
async def emoji(ctx, url: str, *, name):
    guild = ctx.guild
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url) as r:
            try:
                imgOrGif = BytesIO(await r.read())
                eValue = imgOrGif.getvalue()
                if r.status in range(200, 299):
                    emoji = await guild.create_custom_emoji(image=eValue, name=name)
                    await ctx.send(f":{name}: emoji added to your server successfully!")
                    await ses.close()
                else:
                    await ctx.send(f'😞 **Sorry we are unable to add this emoji** | {r.status}')
            except nextcord.HTTPException:
                await ctx.send("📁 Your file size is too big.")


# SUGGESSION COMMAND
@client.command(name="suggestion", aliases=["suggest"], description="You member suggest us something.")
async def suggest(ctx, *, suggestion):
    await ctx.channel.purge(limit=1)
    channel = nextcord.utils.get(ctx.guild.text_channels, name='📨｜suggestions')
    if channel is None:
        await ctx.guild.create_text_channel('📨｜suggestions')
        channel = nextcord.utils.get(
            ctx.guild.text_channels, name='📨｜suggestions')
    suggest = nextcord.Embed(title=f'📝 New Suggestion by {ctx.author.name} !',
                             description=f'{ctx.author.name} has suggested\n ```{suggestion}```', color=0xf20c0c)
    suggest.set_author(
        name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
    suggest.set_footer(
        text=f"Command requested by {ctx.author.name} | 📝 BOT Kernel: 487#G7")
    suggesting = await channel.send(embed=suggest)
    await ctx.send(f"^^ Suggestion ID: {suggesting.id}")
    await suggesting.add_reaction("☑️")
    await suggesting.add_reaction("❌")

""" Making an approve command for suggesion command"""


@client.command(name="approve", description="Approves a suggestion.")
@commands.has_any_role('Admin', 'Moderator', 'Staff', 'Owner')
async def approve(ctx, id: int = None):
    await ctx.channel.purge(limit=1)
    if id is None:
        return
    staff = nextcord.utils.get(ctx.guild.roles, name="Staff")
    if staff is None:
        staff = await ctx.guild.create_role(name="Staff", color=0x51f5e7)
        await ctx.send('Created Role `Staff`. Apply it to start controlling the suggestions.')
    channel = nextcord.utils.get(ctx.guild.text_channels, name="📨｜suggestions")
    achannel = nextcord.utils.get(
        ctx.guild.text_channels, name="✔️approved-suggestions")
    if achannel is None:
        achannel = await ctx.guild.create_text_channel('✔️approved-suggestions')
        await ctx.send("Created `✔️approved-suggestions` channel.Change the channel permission to get started.")
    channel = nextcord.utils.get(ctx.guild.text_channels, name="suggestion")
    if channel is None:
        return
    suggestionMsg = await channel.fetch_message(id)
    embed = nextcord.Embed(title=f'Your suggestion has been approved.',
                           description=f'The suggestion id of `{suggestionMsg.id}` has been approved by {ctx.author.name}', color=0xf20c0c)
    embed.set_author(
        name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
    embed.add_field(name="Link to the embed.",
                    value=f"[Click here ](https://discord.com/channels/{ctx.message.guild.id}/{channel.id}/{suggestionMsg.id}) to see the suggestion.")
    embed.set_footer(
        text=f"Command requested by {ctx.author.name} | 📝 BOT Kernel: 487#G7")
    await achannel.send(embed=embed)

""" Making an deny command for suggesion command"""


@client.command(name="deny", description="Declines a suggestion.")
@commands.has_any_role('Admin', 'Moderator', 'Staff', 'Owner')
async def deny(ctx, id: int = None):
    await ctx.channel.purge(limit=1)
    if id is None:
        return
    staff = nextcord.utils.get(ctx.guild.roles, name="Staff")
    if staff is None:
        staff = await ctx.guild.create_role(name="Staff", color=0x51f5e7)
        await ctx.send('Created Role `Staff`. Apply it to start controlling the suggestions.')
    channel = nextcord.utils.get(ctx.guild.text_channels, name="📨｜suggestions")
    dchannel = nextcord.utils.get(
        ctx.guild.text_channels, name="❌denied-suggestions")
    if dchannel is None:
        dchannel = await ctx.guild.create_text_channel('❌denied-suggestions')
        await ctx.send("Created `❌denied-suggestions` channel.Change the channel permission to get started.")
    if channel is None:
        return
    suggestionMsg = await channel.fetch_message(id)
    embed = nextcord.Embed(title=f'Your suggestion has been denied.',
                           description=f'The suggestion id of `{suggestionMsg.id}` has been denied by {ctx.author.name}', color=0xf20c0c)
    embed.set_author(
        name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
    embed.add_field(name="Link to the embed.",
                    value=f"[Click here ](https://discord.com/channels/{ctx.message.guild.id}/{channel.id}/{suggestionMsg.id}) to see the suggestion.")
    embed.set_footer(
        text=f"Command requested by {ctx.author.name} | 📝 BOT Kernel: 487#G7")
    await dchannel.send(embed=embed)


# GIVEAWAY COMMAND
@client.command(name="giveaway", description="Hosts Giveaway in your server.")
@commands.has_role("🎉Giveaway Host")
async def giveaway(ctx):
    # Giveaway command requires the user to have a "Giveaway Host" role to function properly
    host = nextcord.utils.get(ctx.guild.roles, name="🎉Giveaway Host")
    if host is None:
        host = await ctx.guild.create_role(name="🎉Giveaway Host", color=0x228B22)
        await ctx.send('Created Role `Giveaway Host`. Apply it to start controlling the giveaways.')
    # Stores the questions that the bot will ask the user to answer in the channel that the command was made
    # Stores the answers for those questions in a different list
    giveaway_questions = ['Which channel will I host the giveaway in?', 'What is the prize?', 'How long should the giveaway run for (in seconds)?',]
    giveaway_answers = []

    # Checking to be sure the author is the one who answered and in which channel
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    
    # Askes the questions from the giveaway_questions list 1 by 1
    # Times out if the host doesn't answer within 30 seconds
    for question in giveaway_questions:
        await ctx.send(question)
        try:
            message = await client.wait_for('message', timeout= 30.0, check= check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time.  Please try again and be sure to send your answer within 30 seconds of the question.')
            return
        else:
            giveaway_answers.append(message.content)

    # Grabbing the channel id from the giveaway_questions list and formatting is properly
    # Displays an exception message if the host fails to mention the channel correctly
    try:
        c_id = int(giveaway_answers[0][2:-1])
    except:
        await ctx.send(f'You failed to mention the channel correctly.  Please do it like this: {ctx.channel.mention}')
        return
    
    # Storing the variables needed to run the rest of the commands
    channel = client.get_channel(c_id)
    prize = str(giveaway_answers[1])
    time = int(giveaway_answers[2])

    # Sends a message to let the host know that the giveaway was started properly
    await ctx.send(f'The giveaway for {prize} will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {time} seconds.')

    # Giveaway embed message
    give = nextcord.Embed(color = 0x2ecc71)
    give.set_author(name = f'GIVEAWAY TIME!', icon_url = 'https://i.imgur.com/VaX0pfM.png')
    give.add_field(name= f'{ctx.author.name} is giving away: {prize}!', value = f'React with 🎉 to enter!\n Ends in {round(time/60, 2)} minutes!', inline = False)
    end = datetime.datetime.utcnow() + datetime.timedelta(seconds = time)
    give.set_footer(text = f'Giveaway ends at {end} UTC!')
    my_message = await channel.send(embed = give)
    
    # Reacts to the message
    await my_message.add_reaction("🎉")
    await asyncio.sleep(time)

    new_message = await channel.fetch_message(my_message.id)

    # Picks a winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the winner
    winning_announcement = nextcord.Embed(color = 0xff2424)
    winning_announcement.set_author(name = f'THE GIVEAWAY HAS ENDED!', icon_url= 'https://i.imgur.com/DDric14.png')
    winning_announcement.add_field(name = f'🎉 Prize: {prize}', value = f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}', inline = False)
    winning_announcement.set_footer(text = 'Thanks for entering!')
    await channel.send(embed = winning_announcement)



@client.command(name="reroll", description="Rerolls Giveaway in your server.")
@commands.has_role("🎉Giveaway Host")
async def reroll(ctx, channel: nextcord.TextChannel, id_ : int):
    # Reroll command requires the user to have a "Giveaway Host" role to function properly
    try:
        new_message = await channel.fetch_message(id_)
    except:
        await ctx.send("Incorrect id.")
        return
    
    # Picks a new winner
    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(client.user))
    winner = random.choice(users)

    # Announces the new winner to the server
    reroll_announcement = nextcord.Embed(color = 0xff2424)
    reroll_announcement.set_author(name = f'The giveaway was re-rolled by the host!', icon_url = 'https://i.imgur.com/DDric14.png')
    reroll_announcement.add_field(name = f'🥳 New Winner:', value = f'{winner.mention}', inline = False)
    await channel.send(embed = reroll_announcement)

# UTILITY COMMANDS
# PURGE COMMAND
@client.command(name="clear",description="Clears messages",pass_context=True)
@commands.has_permissions(administrator=True)
async def clear(ctx, limit: int):
        if limit > 101:
            await ctx.send('Cannot delete more than 101 message.')
        else:
            await ctx.channel.purge(limit=limit) 
            await ctx.send(f'Cleared `{limit}` Messgaes')   
            await asyncio.sleep(5)
            await ctx.channel.purge(limit=1) 



# BAN COMMAND
@client.command(name="ban", aliases=["modbancmd"], description="Bans the mentioned user.")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: nextcord.Member, *, reason=None):
    banembed = nextcord.Embed(
        title=f"🔨 Banned {member.name}", description=f"**The {member.name} has been banned from the server due to the following reason:**\n```{reason}```")
    banembed.set_author(
        name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
    banembed.set_footer(
        text=f"Command requested by {ctx.author.name}")
    await member.ban(reason=reason)
    await ctx.send(embed=banembed)


# UNBAN COMMAND
@commands.has_permissions(ban_members=True)
@client.command(name="unban", aliases=["modunban", "removeban"], description="Unbans the mentioned user.")
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            unbanembed = nextcord.Embed(
                title=f"🔨 Unbanned {user.name}", description=f"**The {user.name}#{user.discriminator} has been unbanned from the server .**")
            unbanembed.set_author(
                name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
            unbanembed.set_footer(
                text=f"Command requested by {ctx.author.name}")
            await ctx.send(embed=unbanembed)
            return

# KICK COMMAND
@commands.has_permissions(kick_members=True)
@client.command(name="kick", aliases=["modkickcmd"], description="Kicks the mentioned user.")
async def kick(ctx, member: nextcord.Member, *, reason=None):
    kickembed = nextcord.Embed(
        title=f"🔨 Kicked {member.name}", description=f"**The {member.name} has been kicked from the server due to the following reason:**\n```{reason}```")
    kickembed.set_author(
        name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
    kickembed.set_footer(
        text=f"Command requested by {ctx.author.name}")
    await member.kick(reason=reason)
    await ctx.send(embed=kickembed)


# MUTE  AND UNMUTE COMMAND
@client.command(name="mute", aliases=["modmutecmd"], description="Mutes the mentioned user.")
@commands.has_permissions(ban_members=True, kick_members=True)
async def mute(ctx, member: nextcord.Member, time, *, reason):
    muteembed = nextcord.Embed(
        title=f"🔨 Muted {member.name}", description=f"**The {member.name} has been muted due to the following reason:**\n```{reason}```")
    muteembed.set_author(
        name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
    muteembed.set_footer(
        text=f"Command requested by {ctx.author.name}")
    time = humanfriendly.parse_timespan(time)
    await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=time), reason=reason)
    await ctx.send(embed=muteembed)


@client.command(name="unmute", aliases=["modunmutecmd"], description="Unmutes the mentioned user.")
@commands.has_permissions(ban_members=True, kick_members=True)
async def unmute(ctx, member: nextcord.Member, *, reason):
    unmuteembed = nextcord.Embed(
        title=f"🔨 Unmuted {member.name}", description=f"**The {member.name} has been unmuted due to the following reason:**\n```{reason}```")
    unmuteembed.set_author(
        name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
    unmuteembed.set_footer(
        text=f"Command requested by {ctx.author.name}")
    await member.edit(timeout=None, reason=reason)
    await ctx.send(embed=unmuteembed)

# LOCKDOWN AND UNLOCKDOWN COMMAND
@client.command(name="lockdown", description="Locks the channel mentioned.")
@commands.has_permissions(manage_channels=True)
async def lock(ctx, channel: nextcord.TextChannel = None, setting=None):
    if setting == '--server':
        for channel in ctx.guild.channels:
            lockdownembed = nextcord.Embed(
                title=f":lock: Locked {channel.name}", description=f"**The {channel.name} has been locked because {ctx.author.name} has locked it with --server.")
            lockdownembed.set_author(
                name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
            lockdownembed.set_footer(
                text=f"Command requested by {ctx.author.name}")
            await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked the {channel.name} with --server.", send_messages=False)
            await ctx.send(embed=lockdownembed)
    if channel is None:
        channel = ctx.message.channel
    lockdownembed = nextcord.Embed(
        title=f":lock: Locked {channel.name}", description=f"**The {channel.name} has been locked because {ctx.author.name} has locked it.")
    lockdownembed.set_author(
        name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
    lockdownembed.set_footer(
        text=f"Command requested by {ctx.author.name}")
    await channel.set_permissions(ctx.guild.default_role, reason=f"{ctx.author.name} locked the {channel.name}", send_messages=False)
    await ctx.send(embed=lockdownembed)


@client.command(name="unlockdown", description="Unocks the channel mentioned.")
@commands.has_permissions(manage_channels=True)
async def unlock(ctx, channel: nextcord.TextChannel = None, setting=None):
    if setting == '--server':
        for channel in ctx.guild.channels:
            unlockdownembed = nextcord.Embed(
                title=f":unlock: Unlocked {channel.name}", description=f"**The {channel.name} has been unlocked because {ctx.author.name} has unlocked it with --server.")
            unlockdownembed.set_author(
                name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
            unlockdownembed.set_footer(
                text=f"Command requested by {ctx.author.name}")
            await channel.set_permissions(ctx.guild.default, reason=f"{ctx.author.name} unlocked the {channel.name} with --server", send_messages=True)
            await ctx.send(embed=unlockdownembed)
    if channel is None:
        channel = ctx.message.channel
    unlockdownembed = nextcord.Embed(
        title=f":unlock: Unlocked {channel.name}", description=f"**The {channel.name} has been unlocked because {ctx.author.name} has unlocked it.")
    unlockdownembed.set_author(
        name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
    unlockdownembed.set_footer(
        text=f"Command requested by {ctx.author.name}")
    await channel.set_permissions(ctx.guild.default, reason=f"{ctx.author.name} unlocked the {channel.name}", send_messages=True)
    await ctx.send(embed=unlockdownembed)

# DYNAMIC HELP COMMAND
@client.command(name="help", description="Run this command and get help")
async def help(ctx):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefix = prefixes[str(ctx.guild.id)] 

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

    helpembed = nextcord.Embed(title=":tada: Welcome to the :robot: TechTon Bot help center.",
                               description="**To run a command type** `t!<command>`\n**To learn more about that command type** `t!help <command>`\n __**Checks**__ :\n**1)** `<command signature>` **means this argument is required.**\n**2)**`[command signature]` **means this is optional.**", color=0xb4d3db)
    helpembed.set_author(
        name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")

    for command in client.walk_commands():
        description = command.description
        if not description or description is None or description == "":
            description = "😞 **Sorry we are unable to fetch the description of this command.**"
        helpembed.add_field(
            name=f"`{prefix}{command.name} {command.signature if command.signature is not None else ''}`\n", value=f"{description}\n", inline=False)

    helpembed.set_footer(
        text=f"Command requested by {ctx.author.name}")
    await ctx.send(embed=helpembed)


# Error Handling
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.MissingRequiredArgument):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.MissingRequiredArgument):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.MissingRole):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.MissingPermissions):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.CommandInvokeError):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.CommandOnCooldown):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.ConversionError):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.UserInputError):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)
    if isinstance(error, commands.DisabledCommand):
        notfounderror = nextcord.Embed(
            title="❌ Error in the Bot", description="😞 Sorry we are facing an error while running this command.", color=0xFF5733)
        notfounderror.set_author(
            name="TechTon Bot", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7n64TqeEWHKbR76Ph-kNmE-fz7xlus6-dzQ&usqp=CAU")
        notfounderror.add_field(
            name="Error is described below.", value=f"```\n{error}```")
        notfounderror.add_field(
            name="__**What To do?**__", value="Don't worry we will forward this message to the devs.", inline=False)
        notfounderror.set_footer(
            text=f"Command requested by {ctx.author.name}")
        await ctx.send(embed=notfounderror)

keep_alive()
client.run("OTMyMjY1OTI0NTQxNjgxNzI3.YeQeTQ.dzMizRKrppVo15pbbKfwwjmlozw")
