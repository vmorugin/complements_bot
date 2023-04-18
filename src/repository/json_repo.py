import json
import random
import typing as t

from domains.complements.abstractions import ComplementRepoABC
from domains.complements.model import Complement
from domains.games.abstractions import GameABC, GameRepoABC


class JsonRepo(ComplementRepoABC, GameRepoABC):
    def __init__(self, json_path: str):
        self._path = json_path
        self._base = None

    @property
    def base(self) -> dict:
        if self._base is None:
            self._base = self._parse_json_to_dict(self._path)
        return self._base

    @staticmethod
    @t.final
    def _parse_json_to_dict(json_path) -> dict:
        with open(json_path, 'r') as file:
            return json.load(file)

    def get_games(self) -> list[GameABC]:
        games = self.base.get('games', [])
        return [Converter.game_row_to_obj(game) for game in games]

    def get_game(self, name: str) -> GameABC:
        games = self.base.get('games', [])
        filtered_games = list(filter(lambda x: x.get('name') == name, games))
        if len(filtered_games) == 1:
            return Converter.game_row_to_obj(filtered_games[0])
        raise ValueError('Not found game by name')

    def get_random_complement(self) -> Complement:
        complement = random.choice(self.base.get('complements', []))
        return Converter.complement_row_to_obj(complement)


class Converter:
    @classmethod
    def complement_row_to_obj(cls, row: dict) -> Complement:
        return Complement(
            complement_id=row['id'],
            text=row['text'],
            pic_url=row['pic']
        )

    @classmethod
    def game_row_to_obj(cls, row: dict) -> GameABC:
        return GameABC.make(name=row['name'], title=row['title'])
