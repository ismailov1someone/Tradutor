import os
import threading
from flask import Flask
import telebot
from deep_translator import MyMemoryTranslator

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

TOKEN = os.environ.get("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне текст на русском или португальском, и я его переведу.")

@bot.message_handler(func=lambda message: True)
def translate_text(message):
    text = message.text
    try:
        translated = MyMemoryTranslator(source='pt', target='ru').translate(text)
        if not translated or translated.lower() == text.lower():
            translated = MyMemoryTranslator(source='ru', target='pt').translate(text)
        bot.reply_to(message, translated)
    except Exception:
        bot.reply_to(message, "Произошла ошибка при переводе. Попробуй ещё раз.")

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
