import json
from collections import defaultdict
from itertools import chain

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from domains.games.model import Result
from domains.games.abstractions import GameABC, ResultABC


class CrossAndZeroes(GameABC):
    name = 'CrossAndZeroes'
    row_len = 3
    X_CHAR = '[ X ]'
    O_CHAR = '[ O ]'
    EMPTY_CHAR = '[   ]'
    _last = defaultdict(str)

    def step(self, call: CallbackQuery, **kwargs) -> Result:
        keyboard = self._generate_keyboard(data=kwargs)
        self._last[call.message.chat.id] = self.EMPTY_CHAR
        return Result(text='Крестики-нолики', reply_markup=InlineKeyboardMarkup(keyboard))

    def _generate_keyboard(self, data: dict) -> list[list[InlineKeyboardButton]]:
        callback_data = data.copy()
        callback_data.update({
            'set': True,
        })
        keyboard = []
        for i in range(self.row_len):
            keyboard.append([])
            for j in range(self.row_len):
                callback_data['i'] = i
                callback_data['j'] = j
                keyboard[i].append(InlineKeyboardButton(text=self.EMPTY_CHAR, callback_data=json.dumps(callback_data)))
        return keyboard

    def play(self, call: CallbackQuery, **kwargs) -> ResultABC:
        if self._last[call.message.chat.id] == self.X_CHAR:
            self._last[call.message.chat.id] = self.O_CHAR
        else:
            self._last[call.message.chat.id] = self.X_CHAR
        kwargs['chr'] = self._last[call.message.chat.id]
        keyboard_markup = self._update_keyboard(call, data=kwargs)
        return self._get_end_result(keyboard_markup)

    def _update_keyboard(self, call: CallbackQuery, data: dict) -> InlineKeyboardMarkup:
        i, j = data.get('i'), data.get('j')
        reply_markup = call.message.reply_markup
        if reply_markup.keyboard[i][j].text == self.EMPTY_CHAR:
            reply_markup.keyboard[i][j].text = data['chr']

        return reply_markup

    def _get_end_result(self, keyboard_markup: InlineKeyboardMarkup) -> ResultABC:
        keyboard = keyboard_markup.keyboard
        win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        if self.EMPTY_CHAR not in list(map(lambda x: x.text, chain.from_iterable(keyboard_markup.keyboard))):
            return Result(text=f'[{self.title}]\nНичья', result=True)

        for cord in win_coord:
            elems = [keyboard[col // 3][col % 3] for col in cord]
            if elems[0].text == elems[1].text and elems[1].text == elems[2].text and elems[0].text != self.EMPTY_CHAR:
                return Result(text=f'[{self.title}]\nВыиграли {elems[0].text}', result=True)
        return Result(text='Твой ход', reply_markup=keyboard_markup, result=True)
