import os

from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(token=os.getenv('TELEBOT_TOKEN'))
