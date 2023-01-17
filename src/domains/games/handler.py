import json
import typing as t
from telebot.types import CallbackQuery, InlineKeyboardMarkup

from domains.games.abstractions import GameHandlerABC, GameABC


class GameHandler(GameHandlerABC):

    def filter(self, call: CallbackQuery) -> bool:
        data = self._get_dict_data(call)
        try:
            self._repo.get_game(data.get("name"))
        except ValueError:
            return False
        return True

    @staticmethod
    def _get_dict_data(call: CallbackQuery) -> dict:
        try:
            return json.loads(call.data)
        except json.JSONDecodeError:
            return {}

    async def callback(self, call: CallbackQuery):
        data = self._get_dict_data(call)
        game = self._repo.get_game(data['name'])
        can_play = data.get('set')
        if not can_play:
            return await self._prepare(game, call)

        return await self._play(game, call)

    async def _prepare(self, game: GameABC, call: CallbackQuery):
        result = game.step(call, **self._get_dict_data(call))
        return await self._send_chat_message(call, text=result.text, reply_markup=result.reply_markup)

    async def _play(self, game: GameABC, call: CallbackQuery):
        result = game.play(call, **self._get_dict_data(call))
        if not result:
            return await self.bot.answer_callback_query(call.id, text=result.text)

        return await self._send_chat_message(call, text=result.text, reply_markup=result.reply_markup)

    async def _send_chat_message(self,
                                 call: CallbackQuery,
                                 text: str,
                                 reply_markup: t.Optional[InlineKeyboardMarkup] = None):
        await self.bot.delete_message(call.message.chat.id, call.message.id)
        return await self.bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup)
