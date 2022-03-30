
import time
import nextcord
from nextcord.ext import commands
from TagScriptEngine import Interpreter, block


class Calculator(commands.Cog):
   
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

    @commands.command(aliases=["calc"])
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
        e = nextcord.Embed(
            color=nextcord.Color.green(),
            title=f"Input: `{query}`",
            description=f"Output: `{fmt_str}`",
        )
        e.set_footer(text=f"Calculated in {round((end - start) * 1000, 3)} ms")
        await ctx.send(embed=e)