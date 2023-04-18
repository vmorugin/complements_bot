import abc
import typing as t

from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InlineKeyboardMarkup


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
    def __init__(self, text: str = None, result: bool = False, reply_markup: InlineKeyboardMarkup = None):
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

    def __init__(self, title: str):
        self._title = title

    @property
    def title(self):
        return self._title

    @abc.abstractmethod
    def step(self, call: CallbackQuery, **kwargs) -> ResultABC:
        ...

    @abc.abstractmethod
    def play(self, call: CallbackQuery, **kwargs) -> ResultABC:
        ...

    @t.final
    def _set_prepared(self, params: dict) -> None:
        params['set'] = True


class GameRepoABC(abc.ABC):

    @abc.abstractmethod
    def get_games(self) -> list[GameABC]:
        ...

    @abc.abstractmethod
    def get_game(self, name: str) -> GameABC:
        ...


class GameHandlerABC(abc.ABC):
    def __init__(self, bot: AsyncTeleBot, repo: GameRepoABC):
        self._bot = bot
        self._repo = repo

    @property
    def bot(self):
        return self._bot

    @abc.abstractmethod
    def filter(self, call: CallbackQuery):
        ...

    @abc.abstractmethod
    async def callback(self, call: CallbackQuery):
        ...
