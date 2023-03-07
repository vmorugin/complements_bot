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
        prepared = await self._prepare(game, call)
        if not prepared:
            return await self._send_chat_message(call, text=prepared.text, reply_markup=prepared.reply_markup)

        game_result = await self._play(game, call)
        if not game_result:
            return await self.bot.answer_callback_query(call.id, text=game_result.text)

        return await self._send_chat_message(call, text=game_result.text, reply_markup=game_result.reply_markup)

    async def _prepare(self, game: GameABC, call: CallbackQuery):
        return game.step(call, **self._get_dict_data(call))

    async def _play(self, game: GameABC, call: CallbackQuery):
        return game.play(call, **self._get_dict_data(call))

    async def _send_chat_message(self,
                                 call: CallbackQuery,
                                 text: str,
                                 reply_markup: t.Optional[InlineKeyboardMarkup] = None):
        await self.bot.delete_message(call.message.chat.id, call.message.id)
        return await self.bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup)
