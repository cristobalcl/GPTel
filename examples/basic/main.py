from gptel import GPTelBot, BotContext, ReplyTyping, ReplyImage


bot = GPTelBot(
    name="TestBot",
    description="A bot to test GPTel framework",
    data_default={"flag": False},
)


@bot.command("start", "Starts the bot")
async def command_start(context: BotContext):
    yield rf"Hello {context.user_html}!"


@bot.command("help", "Print some help")
async def command_help(context: BotContext):
    yield r"Help!"


@bot.command("switch", "Switch flag")
async def command_switch(context: BotContext):
    # context.data is specific for current chat.
    context.data["flag"] = not context.data["flag"]
    yield r"Switch on!" if context.data["flag"] else r"Switch off!"


@bot.command("image", "Show an image")
async def command_image(context: BotContext):
    yield ReplyTyping()
    # ReplyImage only supports URL at the moment.
    yield ReplyImage("https://picsum.photos/300/300.jpg")


# This will handle both text chat and voice messages, that will be converted automatically
# to text using OpenAI's Whisper.
@bot.chat()
async def echo(context: BotContext, message: str):
    yield ReplyTyping()
    yield r"You said:"
    yield message


bot.run()
