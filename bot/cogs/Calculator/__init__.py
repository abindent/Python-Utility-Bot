import time
import nextcord
from nextcord.ext import commands
from TagScriptEngine import Interpreter, block
from util.messages import DeleteMessage


__red_end_user_data_statement__ = "This cog does not store any End User Data."

class Calculator(commands.Cog, name="Calculator System", description="Calculate simple math problems like addition, substraction, multiplication, division, etc."):

    COG_EMOJI = "🧮"

    def __init__(self, bot):
        self.bot = bot
        blocks = [
            block.MathBlock(),
            block.RandomBlock(),
            block.RangeBlock(),
        ]
        self.engine = Interpreter(blocks)

    async def red_delete_data_for_user(self, **kwargs):
        return
 
   
    @commands.command(aliases=["calc"], description="Calculate simple math problems like addition, substraction, multiplication, division, etc.", usage="[query (e.g. 1 + 2)]")
    async def calculate(self, ctx, *, query):
        """Math"""
        query = query.replace(",", "")
        engine_input = "{m:" + query + "}"
        start = time.monotonic()
        output = self.engine.process(engine_input)
        end = time.monotonic()

        output_string = output.body.replace("{m:", "").replace("}", "")
        try:
            fmt_str = f"{float(output_string):,}"
        except ValueError:
            fmt_str = output_string
        embed = nextcord.Embed(
            color=nextcord.Color.green(),
            title=f"Input: `{query}`",
            description=f"Output: `{fmt_str}`",
        )
        embed.set_footer(text=f"Calculated in {round((end - start) * 1000, 3)} ms")
        await ctx.send(embed=embed, view=DelBtn(ctx))

