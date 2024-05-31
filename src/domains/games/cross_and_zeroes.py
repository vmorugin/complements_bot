import json
from collections import defaultdict
from itertools import chain
import typing as t

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from domains.games.model import Result
from domains.games.abstractions import GameABC, ResultABC


class CrossAndZeroes(GameABC):
    name = 'CrossAndZeroes'
    ROW_LEN = 3
    X_CHAR = '[ X ]'
    O_CHAR = '[ O ]'
    EMPTY_CHAR = '[   ]'
    _last = defaultdict(str)

    def step(self, call: CallbackQuery, **kwargs) -> Result:
        if self._check_prepared(kwargs):
            return Result(result=True)

        self._set_prepared(kwargs)
        keyboard = self._generate_keyboard(data=kwargs)
        self._last[str(call.message.chat.id)] = self.EMPTY_CHAR
        return Result(text='Крестики-нолики', reply_markup=InlineKeyboardMarkup(keyboard))

    def _generate_keyboard(self, data: dict) -> list[list[InlineKeyboardButton]]:
        callback_data = data.copy()
        keyboard = []
        for i in range(self.ROW_LEN):
            keyboard.append([])
            for j in range(self.ROW_LEN):
                callback_data['i'] = i
                callback_data['j'] = j
                keyboard[i].append(InlineKeyboardButton(text=self.EMPTY_CHAR, callback_data=json.dumps(callback_data)))
        return keyboard

    def play(self, call: CallbackQuery, **kwargs) -> ResultABC:
        if not self._check_can_turn(call, kwargs):
            return Result('Неверный ход')

        kwargs['chr'] = self._switch_turn(str(call.message.chat.id))
        keyboard_markup = self._update_keyboard(call, data=kwargs)
        return self._get_end_result(keyboard_markup)

    def _check_can_turn(self, call: CallbackQuery, data: dict) -> bool:
        i, j = data.get('i'), data.get('j')
        if call.message.reply_markup.keyboard[i][j].text != self.EMPTY_CHAR:
            return False
        return True

    def _switch_turn(self, key: str) -> str:
        if self._last[key] == self.X_CHAR:
            self._last[key] = self.O_CHAR
        else:
            self._last[key] = self.X_CHAR

        return self._last[key]

    @staticmethod
    def _update_keyboard(call: CallbackQuery, data: dict) -> InlineKeyboardMarkup:
        i, j = data.get('i'), data.get('j')
        call.message.reply_markup.keyboard[i][j].text = data['chr']

        return call.message.reply_markup

    def _get_end_result(self, keyboard_markup: InlineKeyboardMarkup) -> ResultABC:
        if win_chr := self._get_win_chr(keyboard_markup.keyboard):
            return Result(text=f'[{self.title}]\nВыиграли {win_chr}', result=True)

        elif self._check_is_draw(keyboard_markup.keyboard):
            return Result(text=f'[{self.title}]\nНичья', result=True)

        return Result(text='Крестики-нолики', reply_markup=keyboard_markup, result=True)

    def _get_win_chr(self, keyboard: list[list[InlineKeyboardButton]]) -> t.Optional[str]:
        win_coord = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))

        for cord in win_coord:
            elems = [keyboard[col // 3][col % 3] for col in cord]
            if elems[0].text == elems[1].text and elems[1].text == elems[2].text and elems[0].text != self.EMPTY_CHAR:
                return elems[0].text

    def _check_is_draw(self, keyboard: list[list[InlineKeyboardButton]]) -> bool:
        if self.EMPTY_CHAR not in list(map(lambda x: x.text, chain.from_iterable(keyboard))):
            return True
        return False
