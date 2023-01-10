import typing as t


class GameCollection:
    __collection = {}

    @classmethod
    def register(cls, name: str, func: t.Callable):
        cls.__collection[name] = func

    @classmethod
    def get_game(cls, name: str) -> t.Callable:
        if name not in cls.__collection:
            raise ValueError(f'Игру {name} я не знаю :(')
        return cls.__collection[name]
