GPTel
=====

Framework to ease the writing of Telegram bots, using advance features like speach to text.

Example
-------

```python
from gptel import GPTelBot, BotContext, ReplyTyping, ReplyImage


bot = GPTelBot(data_default={"flag": False})


@bot.command("start")
async def command_start(context: BotContext):
    yield rf"Hello {context.user_html}!"


@bot.command("help")
async def command_help(context: BotContext):
    yield r"Help!"


@bot.command("switch")
async def command_switch(context: BotContext):
    # context.data is specific for current chat.
    context.data["flag"] = not context.data["flag"]
    yield r"Switch on!" if context.data["flag"] else r"Switch off!"


@bot.command("image")
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
```

Install
-------

```
pip install gptel
```

Setup
-----

You need to setup two environment variables: 

- `TELEGRAM_TOKEN`
- `OPENAI_API_KEY`: for the speech to text service.

To get a new Telegram token for your bot: 

- Open Telegram: Search for `@BotFather`.
- Start a Chat: Click "Start" to begin a conversation with BotFather.
- Create Bot: Send `/newbot` to BotFather.
- Choose Name: Enter a name for your bot when prompted.
- Set Username: Provide a unique username ending in "bot".
- Receive Token: BotFather will give you the bot's token. Keep it secure.

Authors
-------

- Cristobal Carnero Linan - ccarnerolinan@gmail.com
