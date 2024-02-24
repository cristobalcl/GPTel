from gptel import GPTelBot, BotContext


bot = GPTelBot()


@bot.command("help")
async def command_help(bot_context: BotContext):
    yield r"Help!"


bot.run()
