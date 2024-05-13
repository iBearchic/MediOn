import os
from dotenv import load_dotenv
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ConversationHandler)
from utils.utils import (
    DIAGNOSIS, SYMPTOMS, cancel, 
    receive_diagnosis, receive_symptoms, register, 
    start, start_diagnose, status)  

# Загрузка переменных окружения из файла .env
load_dotenv()

def main() -> None:
    """Запуск бота"""

    TOKEN = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('health_record', start_diagnose)],
        states={
            SYMPTOMS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_symptoms)],
            DIAGNOSIS: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_diagnosis)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    # Различные обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("register", register))
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("cancel", cancel))

    # Начинаем поиск обновлений
    application.run_polling()

if __name__ == '__main__':
    main()