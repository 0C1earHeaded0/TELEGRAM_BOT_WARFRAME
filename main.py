import logging
import requests
from telegram import Update, Chat, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

def isServerAvailable():
    if requests.get("https://api.warframestat.us/pc").status_code != 200:
        return False
    else:
        return True

keyboardForCetusStatus = [
    [
        InlineKeyboardButton("ЦЕТУС (РАВНИНЫ ЭЙДОЛОНА)", callback_data='1')
    ],
    [
        InlineKeyboardButton("Камбионский Дрейф (Деймос)", callback_data='2')
    ]
]

keyboard = InlineKeyboardMarkup(keyboardForCetusStatus)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text=
                                   "Привет!👋\n"
                                   "Я бот по игре Warframe!\n"
                                   "Я призван упростить мониторинг за игровыми событиями 😉\n"
                                   "🌍 Выбери локацию с помощью кнопок снизу:",
                                   reply_markup=keyboard)
    if not isServerAvailable():
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="В данный момент сервер не отвечает :(\nВозвращайтесь к нам позже!")
        return



async def cetus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not isServerAvailable():
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="В данный момент сервер не отвечает :(\nВозвращайтесь к нам позже!")
        return
    else:
        cetusStatus = requests.get("https://api.warframestat.us/pc/cetusCycle?language=ru").json()
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=
                                        "--------------\n"
                                        "ЦЕТУС (ЗЕМЛЯ):\n"
                                        "--------------\n"
                                        f"🌍 Сейчас на Цетусе: {"День ☀️" if cetusStatus["isDay"] else 'Ночь 🌑'}\n"
                                        f"⏱️ До смены цикла осталось: {cetusStatus['timeLeft']}\n",
                                        )
async def cambionDrift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not isServerAvailable():
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="В данный момент сервер не отвечает :(\nВозвращайтесь к нам позже!")
        return
    else:
        cambionStatus = requests.get("https://api.warframestat.us/pc/cambionCycle?language=ru").json()
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=
                                        "--------------\n"
                                        "КАМБИОНСКИЙ ДРЕЙФ (ДЕЙМОС):\n"
                                        "--------------\n"
                                        f"🪱 Сейчас царствует: {"Воум" if cambionStatus["state"] == "vome" else "Фэз"}\n"
                                        f"⏱️ До смены цикла осталось: {cambionStatus['timeLeft']}\n",
                                        )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Извини, такой команды у меня пока ещё нет :(")
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    
    if query.data == '1': 
        await cetus(update, context)
    elif query.data == '2':
        await cambionDrift(update, context)
        
    await query.answer()
        
if __name__ == '__main__':
    application = ApplicationBuilder().token('7478612676:AAHw8p8z9ONL7BCDlU8e-rInft1DORKKBi4').build()
    application.add_handler(CommandHandler('start', start)) #Добавляем обработчик событий
    application.add_handler(CommandHandler('cetus', cetus))
    application.add_handler(CommandHandler('cambionDrift', cambionDrift))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.run_polling()
    

    
   #TOKEN: 7478612676:AAHw8p8z9ONL7BCDlU8e-rInft1DORKKBi4