from Service.DateBase.Querty import *
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from telegram import Update, BotCommand, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    ConversationHandler
)
from datetime import datetime

# Загрузка .env
load_dotenv(Path(__file__).parent.parent.parent / '.env')
TOKEN = os.getenv('BOT_TOKEN')

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния для ConversationHandler
NOTE_TEXT, REMINDER_TEXT, REMINDER_TIME = range(3)

# Имитация базы данных в памяти ФЕЙК БАЗЗА ЕПТ
fake_db = {
    'notes': {},
    'reminders': {},
    'next_id': 1
}

# Клавиатура основного меню
def get_main_keyboard():
    return ReplyKeyboardMarkup([
        ["📝 Создать заметку", "📋 Посмотреть заметки"],
    ], resize_keyboard=True)

#настройка команды /strart
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    # Инициализация хранилища для пользователя
    if user_id not in fake_db['notes']:
        fake_db['notes'][user_id] = []
    if user_id not in fake_db['reminders']:
        fake_db['reminders'][user_id] = []
    
    await update.message.reply_text(
        "Добро пожаловать в бота для заметок и напоминаний!",
        reply_markup=get_main_keyboard()
    )

#ФУНКЦИИ ЗАМЕТОК
async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Введите текст заметки: ",
        reply_markup=ReplyKeyboardRemove()
    )
    return NOTE_TEXT

#Cохранение заметок
async def save_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id #получаем уникальное ИД,СООБЩЕНИЕ,ОБЪЕКТ пользователся
    note_text = update.message.text #извлекает текст из сообщение отправленное пользователем боту
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #для создания даты ГОД МЕСЯЦ ДЕНЬ ЧАСЫ МИНУТЫ СЕК

    note_id = fake_db['next_id']
    fake_db['next_id'] += 1 #Увеличивает индекс на +1 для уникальности

    fake_db['notes'][user_id].append({ #Добавляет заметку в базу данных
        'id': note_id,  #ид заметки
        'text': note_text, #текст заметки
        'created_at': created_at #ТАЙМ заметки
    })

    await update.message.reply_text(
        f"✅ Заметка сохранена!\n {note_text}",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

#Просмотр заметок
async def viewing_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    notes = fake_db['notes'].get(user_id, [])
    
    if not notes:
        await update.message.reply_text("У вас пока нет заметок", reply_markup=get_main_keyboard())
        return
    
    response = "📋 Ваши заметки:\n\n"
    for note in notes:
        response += f"🆔 {note['id']}\n📅 {note['created_at']}\n📌 {note['text']}\n\n"
    
    await update.message.reply_text(response, reply_markup=get_main_keyboard())


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Действие отменено",
        reply_markup=get_main_keyboard()
    )
    return ConversationHandler.END

#Установка для меню команд
async def post_init(application: Application):
    commands = [
        BotCommand("note", "Создать заметку"),
        BotCommand("viewing_note", "Посмотреть заметки")
    ]
    await application.bot.set_my_commands(commands)

#интегрируем кнопки на главном меню
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "📝 Создать заметку":
        return await note(update, context)
    elif text == "📋 Посмотреть заметки":
        return await viewing_note(update, context)
    
    await update.message.reply_text("Пожалуйста, используйте кнопки меню или команды")

#ЗАПУСК БОТА
def main():

    application = Application.builder().token(TOKEN).post_init(post_init).build()

#Обработчик создания заметки
    note_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('note', note), #активирует диало при команде /note
                    MessageHandler(filters.Regex('^📝 Создать заметку$'), note)], #активирует диалог при нажатии кнопки
        states={
            NOTE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_note)]
        }, #NOTE_TEXT - состояние ожидания текста заметки, MessageHandler ловит только текстовые сообщения (filters.TEXT), но не команды (~filters.COMMAND), save_note - функция, которая сохранит заметку
        fallbacks=[CommandHandler('cancel', cancel)]
    )

# Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("viewing_note", viewing_note))
    application.add_handler(note_conv_handler) #связывает диалоговый сценариц с работой, без этого ConversationHandler останется неактивным

#Обработчик текстовых сообщений (для кнопок)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    
# Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()

