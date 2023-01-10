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
