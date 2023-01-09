import asyncio
from bot import bot
from repository.complements import ComplementsJsonRepo
from handlers.message import MessageHandler
from settings import BASE_URL


def _setup_bot():
    complements_repo = _setup_complements_repo(BASE_URL / 'database' / 'complements.json')
    _setup_complement_handlers(complements_repo)


def _setup_complements_repo(path: str):
    return ComplementsJsonRepo(path)


def _setup_complement_handlers(repo: ComplementsJsonRepo):
    handler = MessageHandler(repo=repo)
    bot.message_handler(commands=['compliment'])(handler.send_compliment)


def run():
    _setup_bot()
    loop = asyncio.new_event_loop()
    loop.create_task(bot.infinity_polling())
    loop.run_forever()


if __name__ == '__main__':
    run()
