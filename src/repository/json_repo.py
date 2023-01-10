from domains.complements.model import Complement
import random

from domains.games.model import Score
from domains.games.abstractions import GameABC
from repository.abstractions import AbstractJsonRepo, AbstractComplementRepo, AbstractGameRepo


class JsonRepo(AbstractJsonRepo, AbstractComplementRepo, AbstractGameRepo):

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
        return GameABC.make(name=row['name'], title=row['title'], score_cls=Score)
