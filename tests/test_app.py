from typing import Callable, List
import os
import sys

from unittest.mock import patch

from gptel import GPTelBot, AbstractClient, AbstractApplication
from gptel.base import BotCommand, ApplicationConfig


class FakeApplication(AbstractApplication):
    def __init__(self, config: ApplicationConfig):
        super().__init__(config)
        self.run_flag = False
        self.bot_commands: List[BotCommand] = []
        self.chat_handler: Callable = None
        self.audio_handler: Callable = None

    def run(self):
        self.run_flag = True

    def add_handler(self, bot_command: BotCommand):
        self.bot_commands.append(bot_command)

    def set_chat_handler(self, handler: Callable):
        self.chat_handler = handler

    def set_audio_handler(self, handler: Callable):
        self.audio_handler = handler


class FakeClient(AbstractClient):
    def __init__(self):
        pass

    def get_application(self, config=ApplicationConfig) -> AbstractApplication:
        return FakeApplication(config)


class TestBot:
    def test_application(self):
        bot = GPTelBot(
            name="TestBot", description="Test", token="test-token", client=FakeClient()
        )
        assert bot.application.config == ApplicationConfig(
            name="TestBot", description="Test", token="test-token"
        )

    @patch.dict(os.environ, {"TELEGRAM_TOKEN": "test-token-env"})
    def test_environment_token(self):
        bot = GPTelBot(name="TestBot", description="Test", client=FakeClient())
        assert bot.application.config == ApplicationConfig(
            name="TestBot", description="Test", token="test-token-env"
        )

    def test_command(self):
        bot = GPTelBot(
            name="TestBot", description="Test", token="test-token", client=FakeClient()
        )

        @bot.command("test", "A test")
        def command_test():
            pass

        assert bot.bot_commands == [
            BotCommand(command="test", description="A test", handler=command_test)
        ]

    def test_chat_audio(self):
        bot = GPTelBot(
            name="TestBot", description="Test", token="test-token", client=FakeClient()
        )

        @bot.chat()
        def chat_audio_test():
            pass

        assert bot.chat_handler == chat_audio_test
        assert bot.audio_handler == chat_audio_test

    def test_chat(self):
        bot = GPTelBot(
            name="TestBot", description="Test", token="test-token", client=FakeClient()
        )

        @bot.chat(audio=False)
        def chat_test():
            pass

        assert bot.chat_handler == chat_test
        assert bot.audio_handler is None

    def test_audio(self):
        bot = GPTelBot(
            name="TestBot", description="Test", token="test-token", client=FakeClient()
        )

        @bot.audio()
        def audio_test():
            pass

        assert bot.chat_handler is None
        assert bot.audio_handler == audio_test

    @patch.object(sys, "argv", ["foo"])
    def test_run(self):
        bot = GPTelBot(
            name="TestBot", description="Test", token="test-token", client=FakeClient()
        )
        assert not bot.application.run_flag

        @bot.command("help", "Help command")
        async def help():
            print("help")

        @bot.command("hello", "Hello world")
        async def hello():
            print("hello")

        bot.run()
        assert bot.application.bot_commands == [
            BotCommand(command="help", description="Help command", handler=help),
            BotCommand(command="hello", description="Hello world", handler=hello),
        ]
        assert bot.application.run_flag
