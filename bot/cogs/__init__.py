from cogs import About, Activity, Channels, Calculator, Cogs, Config, Docs, Eval, Fun, Games, Help, InviteTracker, Music, Ping, Slash, SubCommands, Suggestion, Moderation
def unload(bot) -> None:
    """
    Reinstates the original help command.
    This is run if the cog raises an exception on load, or if the extension is unloaded.
    """
    bot._old_help = bot.get_command("help")
    bot.remove_command("help")
    bot.add_command(bot._old_help)

def teardown(bot) -> None:
    """
    The teardown for the help extension.
    This is called automatically on `bot.unload_extension` being run.
    Calls `unload` in order to reinstate the original help command.
    """
    unload(bot)

def setup(bot):
    bot.add_cog(About.About(bot))
    bot.add_cog(Activity.Activities(bot))
    bot.add_cog(Channels.Channels(bot))
    bot.add_cog(Calculator.Calculator(bot))
    bot.add_cog(Cogs.CogSetup(bot))
    bot.add_cog(Config.Configuration(bot))
    bot.add_cog(Docs.Docs(bot))
    bot.add_cog(Eval.Eval(bot))
    bot.add_cog(Fun.Fun(bot))
    bot.add_cog(Games.Games(bot))
    bot.add_cog(InviteTracker.InviteTracker(bot))
    bot.add_cog(Music.Music(bot))
    bot.add_cog(Ping.Info(bot))
    bot.add_cog(Slash.Slash(bot))
    bot.add_cog(SubCommands.Groups(bot))
    bot.add_cog(Suggestion.Suggestion(bot))
    bot.add_cog(Moderation.Moderation(bot))
    bot.add_cog(Moderation.ModerationSlash(bot))
    bot.add_cog(Help.Help(bot))

