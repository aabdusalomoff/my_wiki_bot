import telebot
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
from dotenv import load_dotenv
import os

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем токен из .env
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ TELEGRAM_BOT_TOKEN не найден в .env файле")

# Настраиваем бота и язык Википедии
bot = telebot.TeleBot(TOKEN)
wikipedia.set_lang("uz")

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        "Salom! 👋\n"
        "Men Wiki Botman. Menga so'z yoki mavzu yuboring — "
        "men sizga Wikipedia'dan qisqa ma'lumot topib beraman 🔎"
    )

# Обработка всех сообщений
@bot.message_handler(func=lambda message: True)
def get_wiki(message):
    try:
        info = wikipedia.summary(message.text, sentences=3)
        bot.send_message(message.chat.id, info)

    except DisambiguationError as e:
        bot.send_message(message.chat.id, f"Bu so'z bir nechta ma’noga ega. Misollar:\n{', '.join(e.options[:5])}")

    except PageError:
        bot.send_message(message.chat.id, "❌ Bunday maqola topilmadi.")

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Xato yuz berdi, qayta urinib ko‘ring.")

print("✅ Bot ishga tushdi...")
bot.polling(none_stop=True)
