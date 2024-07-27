import logging
import requests
import os
from telegram import Update, Chat, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

async def isServerAvailable():
    if requests.get("https://api.warframestat.us/pc").status_code != 200:
        return False
    else:
        return True
    
keyboardForCetusStatus = [
    [
        InlineKeyboardButton("Равнины Эйдолона (Цетус)", callback_data='1')
    ],
    [
        InlineKeyboardButton("Камбионский Дрейф (Деймос)", callback_data='2')
    ],
    [
        InlineKeyboardButton("Долина Сфер (Фортуна)", callback_data='3')
    ]
]

keyboard = InlineKeyboardMarkup(keyboardForCetusStatus)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not isServerAvailable():
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="В данный момент сервер не отвечает ☹️\nВозвращайтесь к нам позже!")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                    text=
                                    "<b>Привет!👋</b>\n"
                                    "Я бот по игре Warframe!\n"
                                    "Моё призвание - предоставлять информацию о игровых событиях, когда зайти в игру и посмотреть не представляется возможным 😉\n"
                                    "<i><u>🌍 Выбери локацию с помощью кнопок снизу:</u></i>",
                                    reply_markup=keyboard,
                                    parse_mode="HTML")
    
async def cetus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not isServerAvailable():
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="В данный момент сервер не отвечает :(\nВозвращайтесь к нам позже!")
    else:
        cetusStatus = requests.get("https://api.warframestat.us/pc/cetusCycle?language=ru").json()
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=
                                        "--------------\n"
                                        "<b><i>ЦЕТУС (ЗЕМЛЯ):</i></b>\n"
                                        "--------------\n"
                                        f"🌍 Сейчас на Цетусе: <b><u>{"День ☀️" if cetusStatus["isDay"] else 'Ночь 🌑'}</u></b>\n"
                                        f"⏱️ До смены цикла осталось: <b><u>{cetusStatus['timeLeft']}</u></b>\n",
                                        parse_mode="HTML"
                                        )
async def cambionDrift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not isServerAvailable():
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="В данный момент сервер не отвечает :(\nВозвращайтесь к нам позже!")
    else:
        cambionStatus = requests.get("https://api.warframestat.us/pc/cambionCycle?language=ru").json()
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=
                                        "--------------\n"
                                        "<b><i>КАМБИОНСКИЙ ДРЕЙФ (ДЕЙМОС):</i></b>\n"
                                        "--------------\n"
                                        f"🪱 Сейчас царствует: <b><u>{"Воум 🌑" if cambionStatus["state"] == "vome" else "Фэз ☀️"}</u></b>\n"
                                        f"⏱️ До смены цикла осталось: <b><u>{cambionStatus['timeLeft']}</u></b>\n",
                                        parse_mode="HTML"
                                        )
        
async def orbVallis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not isServerAvailable():
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text="В данный момент сервер не отвечает :(\nВозвращайтесь к нам позже!")
    else:
        vallisStatus = requests.get("https://api.warframestat.us/pc/vallisCycle?language=ru").json()
        await context.bot.send_message(chat_id=update.effective_chat.id, 
                                       text=
                                        "--------------\n"
                                        "<b><i>ДОЛИНА СФЕР (ФОРТУНА):</i></b>\n"
                                        "--------------\n"
                                        f"❄️ Сейчас в Долине Сфер: <b><u>{"Тепло ☁️" if vallisStatus["isWarm"] == True else "Холодно 🌨"}</u></b>\n"
                                        f"⏱️ До смены цикла осталось: <b><u>{vallisStatus['timeLeft']}</u></b>\n",
                                        parse_mode="HTML"
                                        )

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="Извини, такой команды у меня пока ещё нет ☹️")
    
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    
    waitingMessage_id = await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=
                                   "<i>Секундочку, я ищу данные о локации... 🤔</i>\n",
                                   parse_mode="HTML")
    
    if query.data == '1': 
        await cetus(update, context)
    elif query.data == '2':
        await cambionDrift(update, context)
    elif query.data == '3':
        await orbVallis(update, context)
        
    await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=waitingMessage_id.message_id)   
    await query.answer()
        
if __name__ == '__main__':
    application = ApplicationBuilder().token(os.environ.get('TOKEN')).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('cetus', cetus))
    application.add_handler(CommandHandler('cambionDrift', cambionDrift))
    application.add_handler(CommandHandler('orbVallis', orbVallis))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.run_polling()