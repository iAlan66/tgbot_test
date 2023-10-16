# -*- coding: UTF-8 -*-
import threading
import time

import requests
import ruamel.yaml
import schedule
import telebot

if __name__ == '__main__':
    yaml = ruamel.yaml.YAML()
    with open('config.yml', encoding="utf-8") as f:
        data = yaml.load(f)
    tg_token = data['tg_token']
    chat_id = data['chat_id']
    bot = telebot.TeleBot(tg_token)


    @bot.message_handler(commands=['history'])
    # 历史上的今天 /history
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

    # 获取名人名言
    def get_sentences():
        api = 'https://api.apiopen.top/api/sentences'
        try:
            response = requests.get(api)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(e)


    @bot.message_handler(commands=['sentence'])
    # 名人名言 /sentence
    def get_sentence(message):
        data = get_sentences()
        result = data["result"]
        bot.send_message(message.chat.id, result["name"] + "——" + result["from"])

    # 定时任务: 名人名言
    def schedule_sentence():
        data = get_sentences()
        result = data["result"]
        bot.send_message(chat_id, result["name"] + "——" + result["from"])

    # 测试定时任务
    def schedule_job():
        bot.send_message(chat_id, "定时任务测试")

    # 定时任务线程
    def schedule_thread():
        # schedule.every(3).seconds.do(schedule_job)
        schedule.every().day.at("09:00").do(schedule_sentence)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def main():
        # 启动定时任务线程
        schedule_t = threading.Thread(target=schedule_thread)
        schedule_t.start()
        # 启动运行 TgBot 线程
        threading.Thread(target=bot.polling).start()

    main()
