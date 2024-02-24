from typing import Callable
from abc import abstractmethod

from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext


class AbstractApplication:
    @abstractmethod
    def run(self):
        pass


class AbstractClient:
    @abstractmethod
    def get_application(self, token: str) -> AbstractApplication:
        pass


class BotContext:
    pass


def telegram_wrapper(handler: Callable) -> Callable:
    async def wrapped_function(update: Update, context: CallbackContext):
        async_gen = handler(TelegramBotContext(update, context))
        async for message in async_gen:
            if isinstance(message, str):
                await update.message.reply_html(message)

    return wrapped_function


class TelegramBotContext(BotContext):
    def __init__(self, update: Update, context: CallbackContext):
        self.update = update
        self.context = context
        self.bot = context.bot
        self.args = context.args
        self.chat_id = update.effective_chat.id if update.effective_chat else None
        self.user = update.effective_user
        self.message = update.message


class TelegramApplication(AbstractApplication):
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()

    def run(self):
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

    def add_handler(self, command: str, handler: Callable):
        self.application.add_handler(CommandHandler(command, telegram_wrapper(handler)))


class TelegramClient(AbstractClient):
    def __init__(self):
        pass

    def get_application(self, token: str) -> AbstractApplication:
        return TelegramApplication(token)
