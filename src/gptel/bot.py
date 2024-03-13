import sys
import os
from typing import Callable, Dict, Optional, List
import asyncio
import argparse

from .base import AbstractClient, BotCommand, ApplicationConfig
from .telegram_client import TelegramClient


class GPTelBot:
    def __init__(
        self,
        name: str,
        description: str,
        data_default: Dict = {},
        token: Optional[str] = None,
        client: Optional[AbstractClient] = None,
    ):
        self.name = name
        self.description = description
        self.data_default = data_default
        self.token = token or os.getenv("TELEGRAM_TOKEN")
        if not self.token:
            raise ValueError("No token")
        self.client = client or TelegramClient()
        self.application = self.client.get_application(
            ApplicationConfig(
                name=self.name,
                description=self.description,
                token=self.token,
                data_default=self.data_default,
            )
        )
        self.bot_commands: List[BotCommand] = []
        self.chat_handler: Optional[Callable] = None
        self.audio_handler: Optional[Callable] = None

    def command(self, command: str, description: str):
        def decorator(func: Callable):
            self.bot_commands.append(
                BotCommand(command=command, description=description, handler=func)
            )
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

    async def asetup(self):
        await self.application.setup()

    def setup(self):
        for command in self.bot_commands:
            self.application.add_handler(command)
        asyncio.run(self.asetup())

    def _parse_arguments(self, arguments):
        parser = argparse.ArgumentParser(description=self.name)
        parser.add_argument("--setup", action="store_true", help="Setup bot")
        return parser.parse_args(arguments)

    def run(self):
        arguments = self._parse_arguments(sys.argv[1:])

        if arguments.setup:
            self.setup()
            return

        for bot_command in self.bot_commands:
            self.application.add_handler(bot_command)
        self.application.set_chat_handler(self.chat_handler)
        self.application.set_audio_handler(self.audio_handler)
        self.application.run()
