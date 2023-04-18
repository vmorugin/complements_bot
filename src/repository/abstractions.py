import abc
import typing as t
import json
from sqlite3 import Connection


class JsonRepoABC(abc.ABC):

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


class SQLiteRepoABC:
    _connection: Connection
