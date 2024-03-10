from abc import abstractmethod
from typing import Callable, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class BotCommand:
    command: str
    description: str
    handler: Callable
    show_in_menu: Optional[bool] = True


@dataclass
class ApplicationConfig:
    name: str
    description: str
    token: str
    data_default: Dict = field(default_factory=dict)


class AbstractApplication:
    data_default: Dict = {}
    config: ApplicationConfig

    def __init__(self, config: ApplicationConfig):
        self.config = config

    @abstractmethod
    async def setup(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def add_handler(self, bot_command: BotCommand):
        pass

    @abstractmethod
    def set_chat_handler(self, handler: Callable):
        pass

    @abstractmethod
    def set_audio_handler(self, handler: Callable):
        pass


class AbstractClient:
    @abstractmethod
    def get_application(self, config: ApplicationConfig) -> AbstractApplication:
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
