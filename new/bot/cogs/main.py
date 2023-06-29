# IMPORTING COGS
from ._sub_command.group import Groups

async def setup(bot):
    await bot.add_cog(Groups(bot))