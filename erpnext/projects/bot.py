
import frappe
import telegram

def send_message(text, chat_id):
    TOKEN = "7280888019:AAE77Ys9GKWjxZpKt10_dsbM6OW_aOm6gGs"
    # chat_id = "-1002771894092"

    bot = telegram.Bot(token=TOKEN)

    try:
        bot.send_message(chat_id=chat_id, text=text)
    except telegram.error.TelegramError as e:
        print(f"Telegram error: {e}")

def send_message_finance(text, chat_id):
    TOKEN = "7280888019:AAE77Ys9GKWjxZpKt10_dsbM6OW_aOm6gGs"
    # chat_id = "-1002771894092"

    bot = telegram.Bot(token=TOKEN)

    try:
        bot.send_message(chat_id=chat_id, text=text)
    except telegram.error.TelegramError as e:
        print(f"Telegram error: {e}")