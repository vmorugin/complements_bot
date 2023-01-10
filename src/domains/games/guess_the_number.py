import random
from itertools import chain
import json
from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


class GuessTheNumberHandler:
    _name = 'GuessTheNumber'

    def __init__(self, bot):
        self._bot: AsyncTeleBot = bot
        self._data = {}

    @property
    def bot(self):
        return self._bot

    def filter(self, call: CallbackQuery):
        data = getattr(call, 'dict_data', {})
        if data.get('type') == 'game' and data.get('name') == "GuessTheNumber":
            self._data = data
            return True
        return False

    def callback(self, call: CallbackQuery):
        result = self._data.get('exp')
        if result is None:
            return self.step_one(call)
        return self.play(call)

    async def step_one(self, call: CallbackQuery):
        keyboard = self._generate_keyboard()
        await self.bot.send_message(call.message.chat.id, text='Выбери число',
                                    reply_markup=InlineKeyboardMarkup(keyboard))

    def _generate_keyboard(self) -> list[list[InlineKeyboardButton]]:
        number_rows = sorted([[random.choice(range(1, 100)) for _ in range(8)] for _ in range(5)])
        self._data.update({
            'exp': random.choice(list(chain.from_iterable(number_rows)))
        })
        keyboard = []
        callback_data = self._data.copy()
        for index, row in enumerate(number_rows):
            keyboard.append([])
            for num in row:
                callback_data['val'] = num
                keyboard[index].append(InlineKeyboardButton(text=num, callback_data=json.dumps(callback_data)))
        return keyboard

    async def play(self, call: CallbackQuery):
        data = getattr(call, 'dict_data', {})
        exp, val = data.get('exp'), data.get('val')
        if exp < val:
            return await self.bot.answer_callback_query(call.id, text='Не-а. Число поменьше')
        elif exp > val:
            return await self.bot.answer_callback_query(call.id, text='Бери больше')
        await self.bot.send_message(call.message.chat.id, text=f'Да, это {val}!!!!! :з Хрю хрю хрю')
