# IMPORTING COGS
from .support.main import Support

async def setup(bot):
    await bot.add_cog(Support(bot))