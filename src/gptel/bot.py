from typing import Optional, Callable, Dict
import os

from .base import AbstractClient
from .telegram_client import TelegramClient


class GPTelBot:
    def __init__(
        self, token: Optional[str] = None, client: Optional[AbstractClient] = None
    ):
        self.token = token or os.getenv("TELEGRAM_TOKEN")
        self.client = client or TelegramClient()
        self.application = self.client.get_application(self.token)
        self.command_handlers: Dict[str, Callable] = {}
        self.chat_handler: Callable = None
        self.audio_handler: Callable = None

    def command(self, command: str):
        def decorator(func: Callable):
            self.command_handlers[command] = func
            return func

        return decorator

    def chat(self, audio: bool = True):
        def decorator(func: Callable):
            self.chat_handler = func
            if audio:
                self.audio_handler = func
            return func

        return decorator

    def audio(self):
        def decorator(func: Callable):
            self.audio_handler = func
            return func

        return decorator

    def run(self):
        for command, handler in self.command_handlers.items():
            self.application.add_handler(command, handler)
        self.application.set_chat_handler(self.chat_handler)
        self.application.set_audio_handler(self.audio_handler)
        self.application.run()
