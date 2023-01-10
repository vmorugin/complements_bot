import json

from telebot import BaseMiddleware
from telebot.types import CallbackQuery


class CallbackMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()
        self.update_types = ['callback_query']

    async def pre_process(self, call: CallbackQuery, data):
        try:
            call.dict_data = json.loads(call.data)
        except json.JSONDecodeError:
            pass

        return call

    async def post_process(self, call: CallbackQuery, data, exception=None):
        return call
