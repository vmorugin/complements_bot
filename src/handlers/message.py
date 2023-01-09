from telebot.types import Message

from src.bot import bot
from repository.abstractions import AbstractComplementRepo


class MessageHandler:
    def __init__(self, repo: AbstractComplementRepo):
        self.repo = repo

    async def send_compliment(self, message: Message):
        complement = self.repo.get_random_complement()
        if complement.pic_url:
            return await bot.send_photo(message.chat.id, photo=complement.pic_url, caption=complement.text)
        return await bot.send_message(message.chat.id, text=complement.text)
