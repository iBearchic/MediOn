import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Загрузка переменных окружения из файла .env
load_dotenv()

async def start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение и помощь по командам."""

    text = "Привет! Я MediON - твой Онлайн Терапевт! \n" \
            "Учусь по симптомам определять наиболее вероятный диагноз.\n" \
            "Буду рад, если Вы поможете своими данными улучшить мои прогнозы!"
    await update.message.reply_text(text)

async def cur_status(update: Update, context: CallbackContext) -> None:
    """Текущее состояние разработки бота"""

    text = "Пока что я нахожусь в разработке..."
    await update.message.reply_text(text)


def main() -> None:
    """Запуск бота"""

    TOKEN = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(TOKEN).build()

    # Различные обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("cur_status", cur_status))

    # Начинаем поиск обновлений
    application.run_polling()

if __name__ == '__main__':
    main()