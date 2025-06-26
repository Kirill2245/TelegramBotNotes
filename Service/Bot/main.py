from Service.DateBase.Querty import *
from dotenv import load_dotenv
from pathlib import Path
import os
import logging
from telegram import Update, BotCommand, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
    ConversationHandler
)
from datetime import datetime

def bot():
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

    # Подключение базы данных
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


    def get_keyboard_add():
        keybutton = [
            [InlineKeyboardButton("Учеба", callback_data='/study')],
            [InlineKeyboardButton("Работа", callback_data='/work')],
            [InlineKeyboardButton("Семья", callback_data='/family')],
            [InlineKeyboardButton("Личное", callback_data='/personal')],
            [InlineKeyboardButton("Прочее", callback_data='/other')],
        ]
        return InlineKeyboardMarkup(keybutton)

    def get_keyboard_check():
        keybutton = [
            [InlineKeyboardButton("Учеба", callback_data='/study_check')],
            [InlineKeyboardButton("Работа", callback_data='/work_check')],
            [InlineKeyboardButton("Семья", callback_data='/family_check')],
            [InlineKeyboardButton("Личное", callback_data='/personal_check')],
            [InlineKeyboardButton("Прочее", callback_data='/other_check')],
            [InlineKeyboardButton("Просмотреть все заметки", callback_data='/all_check')],
        ]
        return InlineKeyboardMarkup(keybutton)


    #настройка команды /strart
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.message.from_user.id
        # Инициализация хранилища для пользователя
        data = {'idUsers': user_id}
        print(user_id)
        if checkUsers(data) == False:
            getUsers(data)
        else:
            print("Пользователь уже существует")
        await update.message.reply_text(
            "Добро пожаловать в бота для заметок и напоминаний!",
            reply_markup=get_main_keyboard()
        )

    async def note_add(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Получаем сообщение в зависимости от типа обновления
        if update.callback_query:
            message = update.callback_query.message
        else:
            message = update.message
        
        await message.reply_text(
            "Введите текст заметки:",
            reply_markup=ReplyKeyboardRemove()
        )
        return NOTE_TEXT

    async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        if query.data == '/study':
            await note_add(update, context)
        # Добавь обработку других callback_data здесь

    #ФУНКЦИИ ЗАМЕТОК
    async def note(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            f'👋 Выберите категорию: \n',
            reply_markup=get_keyboard_add()
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
        await update.message.reply_text(
            f'👋 Выберите категорию: \n',
            reply_markup=get_keyboard_check()
        )
        return NOTE_TEXT
        
        



    async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "Действие отменено",
            reply_markup=get_main_keyboard()
        )
        return ConversationHandler.END

    #Установка для меню команд
    async def post_init(application: Application):
        commands = [
            BotCommand("note_add", "Создать заметку"),
            BotCommand("viewing_note", "Посмотреть заметки")
        ]
        await application.bot.set_my_commands(commands)

    #интегрируем кнопки на главном меню
    async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text
        if text == "📝 Создать заметку":
            await note_add(update, context)
        elif text == "📋 Посмотреть заметки":
            await viewing_note(update, context)
        else:
            await update.message.reply_text("Пожалуйста, используйте кнопки меню!")

    async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        if query.data == '/study':
            await note_add(update, context)
        elif query.data == '/note':
            await note(update, context)
        
        # Добавь обработку других callback_data здесь

    #ЗАПУСК БОТА
    def main():

        application = Application.builder().token(TOKEN).post_init(post_init).build()

    #Обработчик создания заметки
        note_conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('note_add', note_add),
            MessageHandler(filters.Regex('^📝 Создать заметку$'), note),
            CallbackQueryHandler(note_add, pattern='^/study$')
        ],
        states={
            NOTE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, save_note)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Регистрация обработчиков
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("viewing_note", viewing_note))
        application.add_handler(note_conv_handler) #связывает диалоговый сценариц с работой, без этого ConversationHandler останется неактивным
    #Обработчик текстовых сообщений (для кнопок)
        application.add_handler(CallbackQueryHandler(handle_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
        
    # Запуск бота
        application.run_polling()
    if __name__ == '__main__':
        main()
    main()
bot()
