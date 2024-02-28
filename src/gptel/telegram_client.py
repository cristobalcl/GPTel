from typing import Callable, Dict

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from .base import (
    AbstractApplication,
    AbstractClient,
    BotContext,
    ReplyImage,
    ReplyTyping,
)
from .services import TranscriptionClient
from .utils import temporary_file_path


class TelegramBotContext(BotContext):
    def __init__(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        data_default: Dict = {},
    ):
        self.update = update
        self.context = context
        self.bot = context.bot
        self.args = context.args
        self.chat_id = update.effective_chat.id if update.effective_chat else None
        self.user = update.effective_user
        self.message = update.message

        self.user_html = self.user.mention_html()
        self.message = self.update.message.text
        self.tmp_audio_path = None
        self.data = context.chat_data  # A new dictionary should not be created (FIXME)
        for key, value in data_default.items():
            self.data.setdefault(key, value)


async def telegram_send_typing(update, context):
    await context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING
    )


def telegram_wrapper(handler: Callable, data_default: Dict = {}) -> Callable:
    async def wrapped_function(update: Update, context: ContextTypes.DEFAULT_TYPE):
        async_gen = handler(TelegramBotContext(update, context, data_default))
        async for message in async_gen:
            if isinstance(message, str):
                await update.message.reply_html(message)
            elif isinstance(message, ReplyTyping):
                await telegram_send_typing(update, context)
            elif isinstance(message, ReplyImage):
                await update.message.reply_photo(message.url)

    return wrapped_function


def telegram_text_wrapper(handler: Callable) -> Callable:
    async def wrapped_function(context: BotContext):
        async_gen = handler(context, context.message)
        async for message in async_gen:
            yield message

    return wrapped_function


def telegram_audio_wrapper(handler: Callable) -> Callable:
    async def wrapped_function(context: TelegramBotContext):
        yield ReplyTyping()
        with temporary_file_path(suffix=".ogg") as tmp_audio_path:
            context.tmp_audio_path = tmp_audio_path
            file = await context.context.bot.get_file(
                context.update.message.voice.file_id
            )
            await file.download_to_drive(tmp_audio_path)

            transcription_client = TranscriptionClient()
            context.message = await transcription_client.transcript(tmp_audio_path)

            async_gen = handler(context, context.message)
            async for message in async_gen:
                yield message

    return wrapped_function


class TelegramApplication(AbstractApplication):
    def __init__(self, token: str, data_default: Dict = {}):
        self.application = Application.builder().token(token).build()
        self.data_default = data_default

    def run(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def add_handler(self, command: str, handler: Callable):
        self.application.add_handler(
            CommandHandler(command, telegram_wrapper(handler, self.data_default))
        )

    def set_chat_handler(self, handler: Callable):
        self.application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                telegram_wrapper(telegram_text_wrapper(handler), self.data_default),
            )
        )

    def set_audio_handler(self, handler: Callable):
        self.application.add_handler(
            MessageHandler(
                filters.VOICE,
                telegram_wrapper(telegram_audio_wrapper(handler), self.data_default),
            )
        )


class TelegramClient(AbstractClient):
    def __init__(self):
        pass

    def get_application(
        self, token: str, data_default: Dict = {}
    ) -> AbstractApplication:
        return TelegramApplication(token, data_default)
