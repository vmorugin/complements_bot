import abc
from collections import defaultdict


class Game:
    def __init__(self, game_id: int, name: str, title: str):
        self._game_id = game_id
        self._name = name
        self._title = title

    @property
    def name(self):
        return self._name

    @property
    def title(self):
        return self._title


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


class Score(ScoreABC):
    def __init__(self):
        self.__score = defaultdict(int)

    def get(self, key):
        return self.__score.get(key)

    def increase(self, key):
        self.__score[key] += 1

    def pop_key(self, key):
        self.__score.pop(key)

    def clear_all(self):
        self.__score.clear()
