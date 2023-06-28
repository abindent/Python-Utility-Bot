import nextcord
from nextcord.ext import commands
from utils.game_utils import  daily_puzzle_id, generate_info_embed, generate_puzzle_embed, process_message_as_guess, random_puzzle_id, TicTacToe
from utils.delbtn import DelBtnSlashInteractionCheck

from typing import Optional


class Games(commands.Cog):
    
    COG_EMOJI = "🎮"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: nextcord.Message):
        """
        When a message is sent, process it as a guess.
        Then, process any commands in the message if it's not a guess.
        """
        ref = message.reference
        if not ref or not isinstance(ref.resolved, nextcord.Message):
                return False

        else:        
           processed_as_guess = await process_message_as_guess(self.bot, message)
        

    @commands.command(name="tictactoe", description="Playing TicTacToe.....")
    async def tic(self, ctx: commands.Context):
        """Starts a tic-tac-toe game with yourself."""
        await ctx.send('Tic Tac Toe: X goes first', view=TicTacToe())


    @commands.group(invoke_without_command=True, name="wordle", description="Play wordle with me.")
    async def wordle_normal(self, ctx):
       pass

    @wordle_normal.command(name="random", description="Play a random game of Wordle")
    async def slash_play_random_normal(self, ctx):
        embed = generate_puzzle_embed(self.bot, ctx.author, random_puzzle_id())
        await ctx.send(embed=embed)

    @wordle_normal.command(name="id", description="Play a game of Wordle by its ID")
    async def slash_play_id_normal(
        self,
        ctx,
        puzzle_id: int,
    ):
        embed = generate_puzzle_embed(self.bot, ctx.author, puzzle_id)
        await ctx.send(embed=embed)

    @wordle_normal.command(name="daily", description="Play the daily game of Wordle")
    async def slash_play_daily_normal(self, ctx):
        embed = generate_puzzle_embed(self.bot, ctx.author, daily_puzzle_id())
        await ctx.send(embed=embed)

    @wordle_normal.command(name="info", description="Wordle Info")
    async def slash_info_normal(self, ctx):
        await ctx.send(embed=generate_info_embed())

    
    @nextcord.slash_command(name="playwordle", description="Play wordle with me.")
    async def wordle(self, interaction: nextcord.Interaction, option: str= nextcord.SlashOption(name="option", description="Choose an option", choices={"info": "info","random": "random", "daily": "daily", "id": "id"}),  puzzle_id: int = nextcord.SlashOption(description="Puzzle ID of the word to guess", required=False, )):
       if option == "random":   
        embed = generate_puzzle_embed(self.bot, interaction.user, random_puzzle_id())
        await interaction.send(embed=embed, view=DelBtnSlashInteractionCheck(interaction))
       
       elif option == "daily":
        embed = generate_puzzle_embed(self.bot, interaction.user, daily_puzzle_id())
        await interaction.send(embed=embed, view=DelBtnSlashInteractionCheck(interaction))
        
       elif option == "info":
           await interaction.send(embed=generate_info_embed(), view=DelBtnSlashInteractionCheck(interaction)) 
           
       else:
           if option == "id":
              embed = generate_puzzle_embed(self.bot, interaction.user, puzzle_id)
              await interaction.send(embed=embed, view=DelBtnSlashInteractionCheck(interaction))



    


def setup(bot):
    bot.add_cog(Games(bot))
