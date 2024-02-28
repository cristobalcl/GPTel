from typing import Dict, Callable
import os

from unittest.mock import patch

from gptel import GPTelBot, AbstractClient, AbstractApplication


class FakeApplication(AbstractApplication):
    def __init__(self, token: str):
        self.token = token
        self.run_flag = False
        self.command_handlers: Dict[str, Callable] = {}
        self.chat_handler: Callable = None
        self.audio_handler: Callable = None

    def run(self):
        self.run_flag = True

    def add_handler(self, command: str, handler: Callable):
        self.command_handlers[command] = handler

    def set_chat_handler(self, handler: Callable):
        self.chat_handler = handler

    def set_audio_handler(self, handler: Callable):
        self.audio_handler = handler


class FakeClient(AbstractClient):
    def __init__(self):
        pass

    def get_application(
        self, token: str, data_default: Dict = {}
    ) -> AbstractApplication:
        return FakeApplication(token)


class TestBot:
    def test_application(self):
        bot = GPTelBot(token="test-token", client=FakeClient())
        assert bot.application.token == "test-token"

    @patch.dict(os.environ, {"TELEGRAM_TOKEN": "test-token-env"})
    def test_environment_token(self):
        bot = GPTelBot(client=FakeClient())
        assert bot.application.token == "test-token-env"

    def test_command(self):
        bot = GPTelBot(token="test-token", client=FakeClient())

        @bot.command("test")
        def command_test():
            pass

        assert bot.command_handlers["test"] == command_test

    def test_chat_audio(self):
        bot = GPTelBot(token="test-token", client=FakeClient())

        @bot.chat()
        def chat_audio_test():
            pass

        assert bot.chat_handler == chat_audio_test
        assert bot.audio_handler == chat_audio_test

    def test_chat(self):
        bot = GPTelBot(token="test-token", client=FakeClient())

        @bot.chat(audio=False)
        def chat_test():
            pass

        assert bot.chat_handler == chat_test
        assert bot.audio_handler is None

    def test_audio(self):
        bot = GPTelBot(token="test-token", client=FakeClient())

        @bot.audio()
        def audio_test():
            pass

        assert bot.chat_handler is None
        assert bot.audio_handler == audio_test

    def test_run(self):
        bot = GPTelBot(token="test-token", client=FakeClient())
        assert not bot.application.run_flag

        @bot.command("help")
        async def help():
            print("help")

        @bot.command("hello")
        async def hello():
            print("hello")

        bot.run()
        assert bot.application.command_handlers == {"help": help, "hello": hello}
        assert bot.application.run_flag
