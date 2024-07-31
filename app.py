import os

import telebot
import tomllib


class App:
    def __init__(self):
        with open("config.toml", "rb") as f:
            self._conf = tomllib.load(f)
        self._token = self._conf["telegram"]["token"]
        print(self._token)
        self._bot: telebot.TeleBot = telebot.TeleBot(self._token)

    def check_conf(self, key) -> bool:
        return key in self._conf.keys()


    @property
    def bot(self):
        return self._bot

    def polling(self):
        self._bot.infinity_polling()
