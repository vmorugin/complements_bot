from domains.complements.model import Complement
import random

from domains.games.model import Game
from repository.abstractions import AbstractJsonRepo, AbstractComplementRepo, AbstractGameRepo


class JsonRepo(AbstractJsonRepo, AbstractComplementRepo, AbstractGameRepo):

    def get_games_list(self) -> list[Game]:
        games = self.base.get('games', [])
        return [Converter.game_row_to_obj(game) for game in games]

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
    def game_row_to_obj(cls, row: dict) -> Game:
        return Game(game_id=row['id'], name=row['name'], title=row['title'])
