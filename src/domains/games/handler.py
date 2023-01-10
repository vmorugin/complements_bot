import typing as t
from telebot.types import CallbackQuery, InlineKeyboardMarkup

from domains.games.abstractions import GameHandlerABC


class GameHandler(GameHandlerABC):

    def filter(self, call: CallbackQuery):
        data = getattr(call, 'dict_data', {})
        if data.get('name') == self._game.name:
            self._data = data
            return True
        return False

    async def callback(self, call: CallbackQuery):
        can_play = self._data.get('set')
        if not can_play:
            result = self._game.step(call.message, params=self._data)
            return await self._send_chat_message(call, text=result.text, reply_markup=result.reply_markup)

        result = self._game.play(call.message, **self._data)
        if not result:
            return await self.bot.answer_callback_query(call.id, text=result.text)
        return await self._send_chat_message(call, text=result.text)

    async def _send_chat_message(self,
                                 call: CallbackQuery,
                                 text: str,
                                 reply_markup: t.Optional[InlineKeyboardMarkup] = None):
        await self.bot.delete_message(call.message.chat.id, call.message.id)
        return await self.bot.send_message(call.message.chat.id, text=text, reply_markup=reply_markup)
