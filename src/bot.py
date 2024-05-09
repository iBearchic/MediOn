import os
import aiohttp
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ContextTypes

# Загрузка переменных окружения из файла .env
load_dotenv()

async def start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение и помощь по командам."""

    text = "Привет! Я MediON - твой Онлайн Терапевт! \n" \
            "Учусь по симптомам определять наиболее вероятный диагноз.\n" \
            "Буду рад, если Вы поможете своими данными улучшить мои прогнозы!"
    await update.message.reply_text(text)

async def status(update: Update, context: CallbackContext) -> None:
    """Текущее состояние разработки бота"""

    text = "Пока что я нахожусь в разработке..."
    await update.message.reply_text(text)

async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    telegram_nickname = update.effective_user.username
    telegram_id = update.effective_user.id

    if not telegram_nickname:
        await update.message.reply_text("Для регистрации необходимо иметь username в Telegram")
        return

    async with aiohttp.ClientSession() as session:
        async with session.post(
            'http://localhost:8000/register/', 
            json={"telegram_nickname": telegram_nickname, "telegram_id": telegram_id}) as response:
            response_json = await response.json()
            await update.message.reply_text(response_json["message"])


def main() -> None:
    """Запуск бота"""

    TOKEN = os.getenv('TELEGRAM_TOKEN')
    application = Application.builder().token(TOKEN).build()

    # Различные обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("register", register))

    # Начинаем поиск обновлений
    application.run_polling()

if __name__ == '__main__':
    main()