import asyncio
from bot import bot
from bot.middelwares import CallbackMiddleware
from domains.games import GameHandler
from repository.json_repo import JsonRepo
from handlers.message import MessageHandler
from settings import JSON_DB_PATH


def _setup_bot():
    repo = _setup_repo(JSON_DB_PATH.as_posix())
    _setup_handlers(repo)
    _setup_game_callbacks(repo)
    _setup_middlewares()


def _setup_repo(path: str):
    return JsonRepo(path)


def _setup_handlers(repo: JsonRepo):
    handler = MessageHandler(bot, repo=repo)
    bot.message_handler(commands=['compliment'])(handler.send_compliment)
    bot.message_handler(commands=['play_game'])(handler.play_game)


def _setup_game_callbacks(repo):
    _setup_guess_the_number(repo)


def _setup_guess_the_number(repo):
    game = repo.get_game('GuessTheNumber')
    handler = GameHandler(bot, game)
    bot.callback_query_handler(handler.filter)(handler.callback)


def _setup_middlewares():
    bot.setup_middleware(CallbackMiddleware())


def run():
    _setup_bot()
    loop = asyncio.new_event_loop()
    loop.create_task(bot.infinity_polling())
    loop.run_forever()


if __name__ == '__main__':
    run()
