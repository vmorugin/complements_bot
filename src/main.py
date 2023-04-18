import asyncio
import typing as t

from bot import bot
from domains.complements.abstractions import ComplementRepoABC
from domains.games import GameHandler
from domains.games.abstractions import GameRepoABC
from handlers.message import MessageHandler
from repository.sqlite_repo import SQLiteRepo
from settings import SQLITE_PATH


def _setup_bot():
    repo = _setup_repo(SQLITE_PATH.as_posix())
    _setup_handlers(repo)
    _setup_game_callbacks(repo)


def _setup_repo(path: str):
    return SQLiteRepo(path)


def _setup_handlers(repo: t.Union[ComplementRepoABC, GameRepoABC]):
    handler = MessageHandler(bot, repo=repo)
    bot.message_handler(commands=['compliment'])(handler.send_compliment)
    bot.message_handler(commands=['play_game'])(handler.play_game)


def _setup_game_callbacks(repo: GameRepoABC):
    handler = GameHandler(bot, repo)
    bot.callback_query_handler(handler.filter)(handler.callback)


def run():
    _setup_bot()
    loop = asyncio.new_event_loop()
    loop.create_task(bot.infinity_polling())
    loop.run_forever()


if __name__ == '__main__':
    run()
