import random
import sqlite3
import typing as t

from domains.complements.abstractions import ComplementRepoABC
from domains.complements.model import Complement
from domains.games.abstractions import GameRepoABC, GameABC


class SQLiteRepo(ComplementRepoABC, GameRepoABC):
    def __init__(self, path: str):
        self._connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_COLNAMES)

    def get_games(self) -> list[GameABC]:
        row = self._connection.execute(Statements.select_all_games)
        result = row.fetchall()
        return [Converter.make_game(*game) for game in result]

    def get_game(self, name: str) -> GameABC:
        row = self._connection.execute(Statements.select_game_by_name, (name,))
        result = row.fetchone()
        return Converter.make_game(*result)

    def get_random_complement(self) -> Complement:
        total = self._get_count_complements()
        random_id = random.choice(range(total))
        row = self._connection.execute(Statements.select_complement_by_id, (random_id,))
        result = row.fetchone()
        return Converter.make_compliment(*result)

    def _get_count_complements(self) -> int:
        total = self._connection.execute(Statements.count_all_complements)
        res = total.fetchone()
        return res[0]


class Statements:
    count_all_complements = "SELECT count(id) as id from complements"
    select_complement_by_id = "SELECT id, text, pic from complements where id = ?"
    select_all_games = "SELECT name, title from games"
    select_game_by_name = "SELECT name, title from games where name = ?"


class Converter:
    @classmethod
    def make_compliment(cls, compliment_id: int, text: str, pic: t.Optional[str]) -> Complement:
        return Complement(complement_id=compliment_id, text=text, pic_url=pic)

    @classmethod
    def make_game(cls, name: str, title: str) -> GameABC:
        return GameABC.make(name=name, title=title)
