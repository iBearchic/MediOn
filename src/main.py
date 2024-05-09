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

async def echo(update: Update, context: CallbackContext) -> None:
    """Эхо ответ на сообщение пользователя."""

    text = "Пока что я нахожусь в разработке..."
    await update.message.reply_text(text)

def main() -> None:
    """Запуск бота."""
    # Создаем Application и передаем ему токен вашего бота.
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(TOKEN).build()

    # Различные обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Начинаем поиск обновлений
    application.run_polling()

if __name__ == '__main__':
    main()