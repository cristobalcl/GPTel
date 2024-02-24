from gptel import GPTelBot, BotContext


bot = GPTelBot()


@bot.command("help")
async def command_help(bot_context: BotContext):
    pass


bot.run()
