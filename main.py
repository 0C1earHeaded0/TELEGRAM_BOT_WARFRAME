import logging
import requests
from telegram import Update, Chat, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

def isServerAvailable():
    if requests.get("https://api.warframestat.us/pc").status_code != 200:
        return False
    else:
        return True

keyboardForCetusStatus = [
    [
        InlineKeyboardButton("Назад", callback_data='0'),
    ]
]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
) #Функция логирования

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот по игре Warframe!\nЯ призван упростить мониторинг за игровыми событиями, возникающими в ваше отсутствие в игре :)")
    if not isServerAvailable():
        await context.bot.send_message(chat_id=update.effective_chat.id, text="В данный момент сервер не отвечает :(\nВозвращайтесь к нам позже!")
        return

async def cetus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not isServerAvailable():
        await context.bot.send_message(chat_id=update.effective_chat.id, text="В данный момент сервер не отвечает :(\nВозвращайтесь к нам позже!")
    else:
        cetusStatus = requests.get("https://api.warframestat.us/pc/cetusCycle?language=ru").json()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=
                                        "------------------------------------------------------------------------\n"
                                        "ЦЕТУС (ЗЕМЛЯ):\n"
                                        "------------------------------------------------------------------------\n"
                                        f"🌍 Сейчас на Цетусе: {"День ☀️" if cetusStatus["isDay"] else 'Ночь 🌑'}\n"
                                        f"⏱️ До смены цикла осталось: {cetusStatus['timeLeft']}\n",
                                        #reply_markup=InlineKeyboardMarkup(keyboardForCetusStatus)
                                        )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Извини, такой команды у меня пока ещё нет :(")

if __name__ == '__main__':
    application = ApplicationBuilder().token('7478612676:AAHw8p8z9ONL7BCDlU8e-rInft1DORKKBi4').build()
    application.add_handler(CommandHandler('start', start)) #Добавляем обработчик событий
    application.add_handler(CommandHandler('cetus', cetus))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.run_polling()
    

    
   #TOKEN: 7478612676:AAHw8p8z9ONL7BCDlU8e-rInft1DORKKBi4