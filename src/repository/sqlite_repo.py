import random
import sqlite3

from domains.complements.abstractions import ComplementRepoABC
from domains.complements.model import Complement
from domains.games.abstractions import GameRepoABC, GameABC


class SQLiteRepo(ComplementRepoABC, GameRepoABC):
    def __init__(self, path: str):
        self._connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_COLNAMES)
        self._connection.row_factory = self._dict_factory

    @staticmethod
    def _dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def get_games(self) -> list[GameABC]:
        row = self._connection.execute(Statements.select_all_games)
        result = row.fetchall()
        return [Converter.make_game(game) for game in result]

    def get_game(self, name: str) -> GameABC:
        row = self._connection.execute(Statements.select_game_by_name, (name,))
        result = row.fetchone()
        if result is None:
            raise ValueError(f'Not found a game {name}')
        return Converter.make_game(result)

    def get_random_complement(self) -> Complement:
        total = self._get_count_complements()
        random_id = random.choice(range(1, total + 1))
        row = self._connection.execute(Statements.select_complement_by_id, {'id': random_id})
        return Converter.make_compliment(row.fetchone())

    def _get_count_complements(self) -> int:
        total = self._connection.execute(Statements.count_all_complements)
        res = total.fetchone()
        return res['id']


class Statements:
    count_all_complements = "SELECT count(id) as id from complements"
    select_complement_by_id = "SELECT id, text, pic from complements where id=:id"
    select_all_games = "SELECT name, title from games"
    select_game_by_name = "SELECT name, title from games where name = ?"


class Converter:
    @classmethod
    def make_compliment(cls, row: dict) -> Complement:
        return Complement(complement_id=row['id'], text=row['text'], pic_url=row['pic'])

    @classmethod
    def make_game(cls, row: dict) -> GameABC:
        return GameABC.make(name=row['name'], title=row['title'])
