import nextcord, random, datetime
from typing import List
from utils.json import get_path

""" TicTacToe """
class TicTacToeButton(nextcord.ui.Button):
    def __init__(self, x: int, y: int):
        super().__init__(style=nextcord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: nextcord.Interaction):
       assert self.view is not None
       view: TicTacToe = self.view
       state = view.board[self.y][self.x]
       if state in (view.X, view.O):
           return   
       if view.current_player == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
       else:
            self.style = nextcord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

       winner = view.check_board_winner()
       if winner is not None:
            if winner == view.X:
                content = 'X won!'
            elif winner == view.O:
                content = 'O won!'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

       await interaction.response.edit_message(content=content, view=view)    


class TicTacToe(nextcord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None



"""Wordle"""   
EMOJI_CODES = {
    "green": {
        "a": "<:a_green:952504070709575710>",
        "b": "<:b_green:952504071737184276>",
        "c": "<:c_green:952504072823521290>",
        "d": "<:d_green:952504073016475709>",
        "e": "<:e_green:952504073842749511>",
        "f": "<:f_green:952504075277205514>",
        "g": "<:g_green:952504077407903744>",
        "h": "<:h_green:952504078011871245>",
        "i": "<:i_green:952504079479894046>",
        "j": "<:j_green:952504080171950120>",
        "k": "<:k_green:952504084571783188>",
        "l": "<:l_green:952504081912582184>",
        "m": "<:m_green:952504086396276787>",
        "n": "<:n_green:952504084408193044>",
        "o": "<:o_green:952504085465141268>",
        "p": "<:p_green:952504085507080213>",
        "q": "<:q_green:952504087272890378>",
        "r": "<:r_green:952504087851728966>",
        "s": "<:s_green:952504311798169600>",
        "t": "<:t_green:952504312498651137>",
        "u": "<:u_green:952504312922255380>",
        "v": "<:v_green:952504313761107988>",
        "w": "<:w_green:952504314843250698>",
        "x": "<:x_green:952504315799543859>",
        "y": "<:y_green:952504316839755816>",
        "z": "<:z_green:952504317770883132>",
    },
    "yellow": {
        "a": "<:a_yellow:952504348628377650>",
        "b": "<:b_yellow:952504349962170378>",
        "c": "<:c_yellow:952504351002341376>",
        "d": "<:d_yellow:952504351421775872>",
        "e": "<:e_yellow:952504352239669308>",
        "f": "<:f_yellow:952504352575209513>",
        "g": "<:g_yellow:952504355418955776>",
        "h": "<:h_yellow:952504357121830912>",
        "i": "<:i_yellow:952504358048759808>",
        "j": "<:j_yellow:952504363253899294>",
        "k": "<:k_yellow:952504363220348938>",
        "l": "<:l_yellow:952504359835541504>",
        "m": "<:m_yellow:952504366668087336>",
        "n": "<:n_yellow:952504363937579028>",
        "o": "<:o_yellow:952504365028085840>",
        "p": "<:p_yellow:952504365996974120>",
        "q": "<:q_yellow:952504368240922635>",
        "r": "<:r_yellow:952504368853319710>",
        "s": "<:s_yellow:952504369453080576>",
        "t": "<:t_yellow:952504370107396096>",
        "u": "<:u_yellow:952504370753318983>",
        "v": "<:v_yellow:952504371327946802>",
        "w": "<:w_yellow:952504372460408853>",
        "x": "<:x_yellow:952504373785813052>",
        "y": "<:y_yellow:952504374876332102>",
        "z": "<:z_yellow:952504375203491842>",
    },
    "gray": {
        "a": "<:a_grey:952503991336574976>",
        "b": "<:b_grey:952503992385175572>",
        "c": "<:c_grey:952503993110777876>",
        "d": "<:d_grey:952503993752498176>",
        "e": "<:e_grey:952503994205495306>",
        "f": "<:f_grey:952503994582966312>",
        "g": "<:g_grey:952503997011492904>",
        "h": "<:h_grey:952503998940860436>",
        "i": "<:i_grey:952504000002031658>",
        "j": "<:j_grey:952504000824090688>",
        "k": "<:k_grey:952504006217986108>",
        "l": "<:l_grey:952504003080650832>",
        "m": "<:m_grey:952504004896784455>",
        "n": "<:n_grey:952504005978906644>",
        "o": "<:o_grey:952504006612250674>",
        "p": "<:p_grey:952504007547564082>",
        "q": "<:q_grey:952504008860377178>",
        "r": "<:r_grey:952504009653108806>",
        "s": "<:s_grey:952504009799917570>",
        "t": "<:t_grey:952504010626195487>",
        "u": "<:u_grey:952504011196616714>",
        "v": "<:v_grey:952504011779616768>",
        "w": "<:w_grey:952504012358451243>",
        "x": "<:x_grey:952504012954013697>",
        "y": "<:y_grey:952504013474123816>",
        "z": "<:z_grey:952504013742571530>",
    },
}

  

cwd = get_path()
popular_words = open(cwd + "/utils/wordle/popular.txt").read().splitlines()
all_words = set(word.strip() for word in open(cwd + "/utils/wordle/sowpods.txt"))

def generate_colored_word(guess: str, answer: str) -> str:
    """
    Builds a string of emoji codes where each letter is
    colored based on the key:
    - Same letter, same place: Green
    - Same letter, different place: Yellow
    - Different letter: Gray
    Args:
        word (str): The word to be colored
        answer (str): The answer to the word
    Returns:
        str: A string of emoji codes
    """
    colored_word = [EMOJI_CODES["gray"][letter] for letter in guess]
    guess_letters = list(guess)
    answer_letters = list(answer)
    # change colors to green if same letter and same place
    for i in range(len(guess_letters)):
        if guess_letters[i] == answer_letters[i]:
            colored_word[i] = EMOJI_CODES["green"][guess_letters[i]]
            answer_letters[i] = None
            guess_letters[i] = None
    # change colors to yellow if same letter and not the same place
    for i in range(len(guess_letters)):
        if guess_letters[i] is not None and guess_letters[i] in answer_letters:
            colored_word[i] = EMOJI_CODES["yellow"][guess_letters[i]]
            answer_letters[answer_letters.index(guess_letters[i])] = None
    return "".join(colored_word)


def generate_blanks() -> str:
    """
    Generate a string of 5 blank white square emoji characters
    Returns:
        str: A string of white square emojis
    """
    return "\N{WHITE MEDIUM SQUARE}" * 5


def generate_puzzle_embed(bot, user: nextcord.User, puzzle_id: int) -> nextcord.Embed:
    """
    Generate an embed for a new puzzle given the puzzle id and user
    Args:
        user (nextcord.User): The user who submitted the puzzle
        puzzle_id (int): The puzzle ID
    Returns:
        nextcord.Embed: The embed to be sent
    """
    embed = nextcord.Embed(title="🎲 | **Play `Wordle` with me**", description="\n".join([generate_blanks()] * 6 ), color=nextcord.Color.blue())
    embed.description = "\n".join([generate_blanks()] * 6)
    embed.set_author(name="OpenSource Utility Bot", icon_url=bot.user.display_avatar)
    embed.set_author(name=user.name, icon_url=user.display_avatar.url)
    embed.set_footer(
        text=f"ID: {puzzle_id} ︱ To play, use the command /play!\n"
        "To guess, reply to this message with a word."
    )
    return embed


def update_embed(embed: nextcord.Embed, guess: str) -> nextcord.Embed:
    """
    Updates the embed with the new guesses
    Args:
        embed (nextcord.Embed): The embed to be updated
        puzzle_id (int): The puzzle ID
        guess (str): The guess made by the user
    Returns:
        nextcord.Embed: The updated embed
    """
    puzzle_id = int(embed.footer.text.split()[1])
    answer = popular_words[puzzle_id]
    colored_word = generate_colored_word(guess, answer)
    empty_slot = generate_blanks()
    # replace the first blank with the colored word
    embed.description = embed.description.replace(empty_slot, colored_word, 1)
    # check for game over
    num_empty_slots = embed.description.count(empty_slot)
    if guess == answer:
        if num_empty_slots == 0:
            embed.description += "\n\nPhew!"
        if num_empty_slots == 1:
            embed.description += "\n\nGreat!"
        if num_empty_slots == 2:
            embed.description += "\n\nSplendid!"
        if num_empty_slots == 3:
            embed.description += "\n\nImpressive!"
        if num_empty_slots == 4:
            embed.description += "\n\nMagnificent!"
        if num_empty_slots == 5:
            embed.description += "\n\nGenius!"
    elif num_empty_slots == 0:
        embed.description += f"\n\nThe answer was {answer}!"
    return embed


def is_valid_word(word: str) -> bool:
    """
    Validates a word
    Args:
        word (str): The word to validate
    Returns:
        bool: Whether the word is valid
    """
    return word in all_words


def random_puzzle_id() -> int:
    """
    Generates a random puzzle ID
    Returns:
        int: A random puzzle ID
    """
    return random.randint(0, len(popular_words) - 1)


def daily_puzzle_id() -> int:
    """
    Calculates the puzzle ID for the daily puzzle
    Returns:
        int: The puzzle ID for the daily puzzle
    """
    # calculate days since 1/1/2022 and mod by the number of puzzles
    num_words = len(popular_words)
    time_diff = datetime.datetime.now().date() - datetime.date(2022, 1, 1)
    return time_diff.days % num_words


def is_game_over(embed: nextcord.Embed) -> bool:
    """
    Checks if the game is over in the embed
    Args:
        embed (nextcord.Embed): The embed to check
    Returns:
        bool: Whether the game is over
    """
    return "\n\n" in embed.description


def generate_info_embed() -> nextcord.Embed:
    """
    Generates an embed with information about the bot
    Returns:
        nextcord.Embed: The embed to be sent
    """
    join_url = "https://discord.com/api/oauth2/authorize?client_id=932265924541681727&permissions=11264&scope=bot%20applications.commands"
    discord_url = "https://discord.io/OpenSourceGames"
    youtube_url = "https://tiny.cc/DiscoHuge-YT"
    github_url = "https://github.com/abindent/Nextcord-Utility-Bot"
    return nextcord.Embed(
        title="About Wordle",
        description=(
            "Discord Wordle is a game of wordle-like puzzle solving.\n\n"
            "**You can start a game with**\n\n"
            ":sunny: `/playwordle daily` - Play the puzzle of the day\n"
            ":game_die: `/playwordle random` - Play a random puzzle\n"
            ":boxing_glove: `/playwordle id <puzzle_id>` - Play a puzzle by ID\n\n"
            f"<:member_join:942985122846752798> [Add this bot to your server]({join_url})\n"
            f"<:discord:942984508586725417> [Join my Discord server]({discord_url})\n"
            f"<:youtube:942984508976795669> [YouTube tutorial on the making of this bot]({youtube_url})\n"
            f"<:github:942984509673066568> [View the source code on GitHub]({github_url})\n"
        ),
    )


async def process_message_as_guess(
    bot: nextcord.Client, message: nextcord.Message
) -> bool:
    """
    Check if a new message is a reply to a Wordle game.
    If so, validate the guess and update the bot's message.
    Args:
        bot (nextcord.Client): The bot
        message (nextcord.Message): The new message to process
    Returns:
        bool: True if the message was processed as a guess, False otherwise
    """
    # get the message replied to
    ref = message.reference
    if not ref or not isinstance(ref.resolved, nextcord.Message):
        return False
    parent = ref.resolved

    # if the parent message is not the bot's message, ignore it
    if parent.author.id != bot.user.id:
        return False

    # check that the message has embeds
    if not parent.embeds:
        return False

    embed = parent.embeds[0]

    guess = message.content.lower()

    # check that the user is the one playing
    if (
        embed.author.name != message.author.name
        or embed.author.icon_url != message.author.display_avatar.url
    ):
        reply = "Start a new game with /play"
        if embed.author:
            reply = f"This game was started by {embed.author.name}. " + reply
        await message.reply(reply, delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the game is not over
    if is_game_over(embed):
        await message.reply(
            "The game is already over. Start a new game with /play", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that a single word is in the message
    if len(message.content.split()) > 1:
        await message.reply(
            "Please respond with a single 5-letter word.", delete_after=5
        )
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # check that the word is valid
    if not is_valid_word(guess):
        await message.reply("That is not a valid word", delete_after=5)
        try:
            await message.delete(delay=5)
        except Exception:
            pass
        return True

    # update the embed
    embed = update_embed(embed, guess)
    await parent.edit(embed=embed)

    # attempt to delete the message
    try:
        await message.delete()
    except Exception:
        pass

    return True
