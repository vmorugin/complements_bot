import abc
import typing as t

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup, Message


class ScoreABC(abc.ABC):

    @abc.abstractmethod
    def get(self, key) -> int:
        ...

    @abc.abstractmethod
    def increase(self, key):
        ...

    @abc.abstractmethod
    def pop_key(self, key) -> int:
        ...

    @abc.abstractmethod
    def clear_all(self):
        ...


class GameMeta(abc.ABCMeta):
    __GAME_COLLECTION: dict[str, t.Type["GameABC"]] = {}

    def __new__(mcs, name: str, bases: t.Tuple[t.Type], attrs: dict):
        cls = super().__new__(mcs, name, bases, attrs)
        mcs._register_message_class(cls)  # noqa
        return cls

    @classmethod
    def _register_message_class(mcs, cls):
        if hasattr(cls, 'name'):
            mcs.__GAME_COLLECTION[str(cls.name)] = cls

    def make(cls, name: str, **kwargs):
        if name not in cls.__GAME_COLLECTION:
            raise ValueError('Not found game')
        klass = cls.__GAME_COLLECTION[name]
        return klass(**kwargs)  # noqa


class ResultABC(abc.ABC):
    def __init__(self, text: str, result: bool = False, reply_markup: InlineKeyboardMarkup = None):
        self._result = result
        self._text = text
        self._reply_markup = reply_markup

    @property
    def result(self) -> bool:
        return self._result

    @property
    def text(self) -> str:
        return self._text

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        return self._reply_markup

    @t.final
    def __bool__(self):
        return self._result


class GameABC(abc.ABC, metaclass=GameMeta):
    name: str

    def __init__(self, title: str, score_cls: t.Type[ScoreABC]):
        self._title = title
        self._score = score_cls()

    @property
    def title(self):
        return self._title

    def step(self, message: Message, params: dict) -> ResultABC:
        ...

    @abc.abstractmethod
    def play(self, message: Message, **kwargs) -> ResultABC:
        ...


class GameHandlerABC(abc.ABC):
    def __init__(self, bot: AsyncTeleBot, game: GameABC):
        self._bot = bot
        self._game = game
        self._data = {}

    @property
    def bot(self):
        return self._bot

    @abc.abstractmethod
    def filter(self, call: CallbackQuery):
        ...

    @abc.abstractmethod
    async def callback(self, call: CallbackQuery):
        ...
