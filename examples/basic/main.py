from gptel import GPTelBot, BotContext, ReplyTyping, ReplyImage


bot = GPTelBot()


@bot.command("start")
async def command_start(context: BotContext):
    yield rf"Hello {context.user_html}!"


@bot.command("help")
async def command_help(context: BotContext):
    yield r"Help!"


@bot.command("image")
async def command_image(context: BotContext):
    yield ReplyTyping()
    yield ReplyImage("https://picsum.photos/300/300.jpg")


@bot.chat()
async def echo(context: BotContext, message: str):
    yield ReplyTyping()
    yield r"You said:"
    yield message


bot.run()
