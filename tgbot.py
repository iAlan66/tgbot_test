# -*- coding: UTF-8 -*-
import ruamel.yaml
import requests

import telebot

if __name__ == '__main__':
    yaml = ruamel.yaml.YAML()
    with open('config.yml', encoding="utf-8") as f:
        data = yaml.load(f)
    tg_token = data['tg_token']
    bot = telebot.TeleBot(tg_token)

    @bot.message_handler(commands=['history'])
    def today_history(message):
        api = 'https://api.oick.cn/lishi/api.php'
        try:
            response = requests.get(api)
            if response.status_code == 200:
                data = response.json()
                result = "历史上的今天:\n"
                num = 0
                for i in data["result"]:
                    num += 1
                    result += str(num) + ". " + i["date"] + ": " + i["title"] + "\n"
                bot.send_message(message.chat.id, result)
        except Exception as e:
            print(e)

    def main():
        bot.infinity_polling()
    main()

