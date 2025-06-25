from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, ContextTypes

# Загрузка .env
load_dotenv(Path(__file__).parent.parent.parent / '.env')
TOKEN = os.getenv('BOT_TOKEN')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("........")

async def viewing_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("........")

async def delete_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("........")

async def clear_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("........")

async def reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("........")

async def reminder_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("........")

async def delete_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("........")

async def clear_reminder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("........")


async def post_init(application: Application):
    """Установка меню команд бота"""
    commands = [
        BotCommand("note", "Создать заметку"),
        BotCommand("viewing_note", "Посмотреть заметки"),
        BotCommand("delete_note", "Удалить заметку"),
        BotCommand("clear_note", "Удалить все заметки"),
        BotCommand("reminder", "Создать напоминание"),
        BotCommand("reminder_note", "Посмотреть напоминание"),
        BotCommand("delete_reminder", "Удалить напоминание"),
        BotCommand("clear_reminder", "Удалить все напоминания"),
    ]
    await application.bot.set_my_commands(commands)

def main():
    """Запуск бота"""
    application = (
    Application.builder()
    .token(TOKEN)
    .post_init(post_init)
    .build()
)

    # Регистрация обработчиков
    application.add_handler(CommandHandler("note", note))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()