from typing import Optional, Callable, Dict
import os

from .client import AbstractClient, TelegramClient


class GPTelBot:
    def __init__(self, token: Optional[str] = None, client: Optional[AbstractClient] = None):
        self.token = token or os.getenv("TELEGRAM_TOKEN")
        self.client = client or TelegramClient()
        self.application = self.client.get_application(self.token)
        self.command_handlers: Dict[str, Callable] = {}

    def command(self, command: str):
        def decorator(func: Callable):
            self.command_handlers[command] = func
            return func
        return decorator

    def run(self):
        for command, handler in self.command_handlers.items():
            self.application.add_handler(command, handler)
        self.application.run()
