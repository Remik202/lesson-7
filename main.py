import ptbot

import os
from dotenv import load_dotenv

from pytimeparse import parse


def notify_progress(secs_left, chat_id, message_id, total_seconds):
    elapsed_time = total_seconds - secs_left  
    progressbar = render_progressbar(total_seconds, elapsed_time)
    bot.update_message(
        chat_id, message_id, f"Прошло {elapsed_time} секунд! {progressbar}"
    )

def wait(chat_id, answer):
    seconds = parse(answer)
    if seconds is None:
        bot.send_message(chat_id, "Пожалуйста, введите корректное время (например, '8s').")
        return
    message_id = bot.send_message(chat_id, seconds)

    bot.create_countdown(
        seconds, notify_progress, chat_id=chat_id, message_id=message_id, total_seconds=seconds
    )
    bot.create_timer(seconds, choose, chat_id=chat_id, answer=answer)

def render_progressbar(total, iteration, prefix="", suffix="", length=30, fill="█", zfill="░"):
    iteration = min(total, iteration)
    percent = "{0:.1f}".format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return "{0} |{1}| {2}% {3}".format(prefix, pbar, percent, suffix)


def choose(chat_id, answer):
    answer = "Время вышло!"
    bot.send_message(chat_id, answer)


def main():
    load_dotenv()
    global telegram_token
    global bot
    telegram_token = os.getenv("TG_TOKEN")
    bot = ptbot.Bot(telegram_token)
    bot.reply_on_message(wait)
    bot.run_bot()


if __name__ == "__main__":
    main()