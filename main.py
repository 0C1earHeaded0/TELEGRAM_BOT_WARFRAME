import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот по игре Warframe!\nЯ призван упростить мониторинг за игровыми событиями, возникающими в ваше отсутствие в игре :)")

if __name__ == '__main__':
    application = ApplicationBuilder().token('7478612676:AAHw8p8z9ONL7BCDlU8e-rInft1DORKKBi4').build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling() #Ждёт ввода пользователя
    
    
   # 7478612676:AAHw8p8z9ONL7BCDlU8e-rInft1DORKKBi4