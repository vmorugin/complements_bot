import json
import random

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from domains.games.model import Result
from domains.games.abstractions import GameABC


class GuessTheNumberGame(GameABC):
    name = 'GuessTheNumber'

    def play(self, message: Message, **kwargs):
        self._score.increase(message.id)
        tries = self._score.get(message.id)
        expected, real = kwargs.get('set'), kwargs.get('val')
        if expected < real:
            return Result(text='Не-а. Число поменьше')
        elif expected > real:
            return Result(text='Бери больше')
        self._score.pop_key(message.id)
        return Result(text=f'[{self.title}]\nДа, это {real}!!!!! :з Хрю хрю хрю.\nС {tries} попытки!', result=True)

    def step(self, message: Message, params: dict) -> Result:
        rows = 8
        keyboard = self._generate_keyboard(rows=rows, data=params)
        return Result(text='Выбери число', reply_markup=InlineKeyboardMarkup(keyboard, row_width=rows))

    @staticmethod
    def _generate_keyboard(rows: int, data: dict) -> list[list[InlineKeyboardButton]]:
        numbers = 96
        numbers_list = [num for num in range(numbers, 0, -1)]
        callback_data = data.copy()
        callback_data.update({
            'set': random.choice(numbers_list),
        })
        keyboard = []
        for i in range(int(numbers / rows)):
            keyboard.append([])
            for j in range(rows):
                num = numbers_list.pop()
                callback_data['val'] = num
                keyboard[i].append(InlineKeyboardButton(text=num, callback_data=json.dumps(callback_data)))
        return keyboard
