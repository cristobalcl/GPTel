from abc import abstractmethod
from typing import Callable, Dict


class AbstractApplication:
    data_default: Dict = {}

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def add_handler(self, command: str, handler: Callable):
        pass

    @abstractmethod
    def set_chat_handler(self, handler: Callable):
        pass

    @abstractmethod
    def set_audio_handler(self, handler: Callable):
        pass


class AbstractClient:
    @abstractmethod
    def get_application(
        self, token: str, data_default: Dict = {}
    ) -> AbstractApplication:
        pass


class ReplyBase:
    pass


class ReplyTyping(ReplyBase):
    pass


class ReplyImage(ReplyBase):
    url: str

    def __init__(self, url: str):
        self.url = url


class BotContext:
    def __init__(self):
        self.user_html = ""
        self.message = ""
        self.tmp_audio_path = None
        self.data = {}
