import os

from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(token=os.environ['TELEBOT_TOKEN'])
