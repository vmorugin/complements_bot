import json
import typing as t
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from telebot.async_telebot import AsyncTeleBot

from domains.complements.abstractions import ComplementRepoABC
from domains.games.abstractions import GameRepoABC


class MessageHandler:
    def __init__(self, bot: AsyncTeleBot, repo: t.Union[ComplementRepoABC, GameRepoABC]):
        self.repo = repo
        self.bot = bot

    async def send_compliment(self, message: Message):
        complement = self.repo.get_random_complement()
        await self.bot.delete_message(message.chat.id, message.id)
        if complement.pic_url:
            return await self.bot.send_photo(message.chat.id, photo=complement.pic_url, caption=complement.text)
        return await self.bot.send_message(message.chat.id, text=complement.text)

    async def play_game(self, message: Message):
        games = self.repo.get_games()
        keyboard = []
        for game in games:
            callback_data = json.dumps({"name": game.name})
            keyboard.append([InlineKeyboardButton(text=game.title, callback_data=callback_data)])
        await self.bot.delete_message(message.chat.id, message.id)
        await self.bot.send_message(message.chat.id, text='В какую игру играем?',
                                    reply_markup=InlineKeyboardMarkup(keyboard=keyboard))
