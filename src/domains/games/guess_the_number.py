import asyncio
import random
import json
import typing as t
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from domains.games.model import ScoreABC


class GuessTheNumberHandler:
    _name: str = 'GuessTheNumber'

    def __init__(self, bot, score: t.Type[ScoreABC]):
        self._bot: AsyncTeleBot = bot
        self._score = score()
        self._data = {}

    @property
    def bot(self):
        return self._bot

    def filter(self, call: CallbackQuery):
        data = getattr(call, 'dict_data', {})
        if data.get('name') == self._name:
            self._data = data
            return True
        return False

    def callback(self, call: CallbackQuery):
        result = self._data.get('exp')
        if result is None:
            return self.step_one(call)
        return self.play(call)

    async def step_one(self, call: CallbackQuery):
        rows = 8
        keyboard = self._generate_keyboard(rows=rows)
        await self._send_chat_message(call, text='Выбери число',
                                      reply_markup=InlineKeyboardMarkup(keyboard, row_width=rows))

    async def _send_chat_message(self,
                                 call: CallbackQuery,
                                 text: str,
                                 reply_markup: t.Optional[InlineKeyboardMarkup] = None):
        await self.bot.delete_message(call.message.chat.id, call.message.id)
        return await self.bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup)

    def _generate_keyboard(self, rows: int) -> list[list[InlineKeyboardButton]]:
        numbers = 96
        numbers_list = [num for num in range(numbers, 0, -1)]
        self._data.update({
            'exp': random.choice(numbers_list)
        })
        callback_data = self._data.copy()
        keyboard = []
        for i in range(int(numbers / rows)):
            keyboard.append([])
            for j in range(rows):
                num = numbers_list.pop()
                callback_data['val'] = num
                keyboard[i].append(InlineKeyboardButton(text=num, callback_data=json.dumps(callback_data)))
        return keyboard

    async def play(self, call: CallbackQuery):
        self._score.increase(call.message.id)
        tries = self._score.get(call.message.id)
        data = getattr(call, 'dict_data', {})
        exp, val = data.get('exp'), data.get('val')
        if exp < val:
            return await self.bot.answer_callback_query(call.id, text='Не-а. Число поменьше')
        elif exp > val:
            return await self.bot.answer_callback_query(call.id, text='Бери больше')
        message = await self._send_chat_message(call, text=f'Да, это {val}!!!!! :з Хрю хрю хрю.\nС {tries} попытки!')
        self._score.pop_key(call.message.id)
        await asyncio.sleep(10)
        await self.bot.delete_message(message.chat.id, message.id)
