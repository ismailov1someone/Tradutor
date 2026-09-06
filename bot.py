import os
import telebot
from deep_translator import MyMemoryTranslator

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

bot.infinity_polling()
