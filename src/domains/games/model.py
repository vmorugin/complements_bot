from collections import defaultdict

from domains.games.abstractions import ScoreABC, ResultABC


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


class Result(ResultABC):
    ...
