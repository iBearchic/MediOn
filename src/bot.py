import os
import aiohttp
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters,
    CallbackContext, ContextTypes, ConversationHandler)
from utils.utils import check_user_registration

# Загрузка переменных окружения из файла .env
load_dotenv()

async def start(update: Update, context: CallbackContext) -> None:
    """Отправляет приветственное сообщение и помощь по командам."""

    text = "Привет! Я MediON - твой Онлайн Терапевт! \n" \
            "Учусь по симптомам определять наиболее вероятный диагноз.\n" \
            "Буду рад, если Вы поможете своими данными улучшить мои прогнозы! \n \n" \
            "Нажми на команду /status, чтобы узнать мои возможности"
    await update.message.reply_text(text)

async def status(update: Update, context: CallbackContext) -> None:
    """Текущее состояние разработки бота"""

    text = "Пока что я нахожусь в разработке...\n" \
            "Вместе с тем уже знаю несколько команд: \n" \
            "/register - Регистрация нового пользователя для использования всего функционала бота\n" \
            "/health_record - Запись симптомов и предполагаемого диагноза для расширения базы знаний\n" \
            "/cancel - Отмена текущего действия"
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

# Определение состояний
SYMPTOMS, DIAGNOSIS = range(2)

async def start_diagnose(update: Update, context: CallbackContext) -> int:
    telegram_id = update.effective_user.id
    is_registered = await check_user_registration(telegram_id)
    if not is_registered:
        await update.message.reply_text("Вы не зарегистрированы. Пожалуйста, сначала зарегистрируйтесь, используя команду /register")
        return ConversationHandler.END
    await update.message.reply_text("Пожалуйста, опишите ваши симптомы:")
    return SYMPTOMS

async def receive_symptoms(update: Update, context: CallbackContext) -> int:
    context.user_data['symptoms'] = update.message.text
    await update.message.reply_text("Пожалуйста, введите предполагаемый диагноз:")
    return DIAGNOSIS

async def receive_diagnosis(update: Update, context: CallbackContext) -> int:
    diagnosis = update.message.text
    telegram_id = update.effective_user.id
    symptoms = context.user_data['symptoms']

    url = "http://localhost:8000/health_record/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"symptoms": symptoms, "disease": diagnosis, "telegram_id": telegram_id}) as response:
            response_json = await response.json()
            await update.message.reply_text(response_json["message"])

    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Диагностика отменена! Как будете готовы - попробуем еще раз!")
    return ConversationHandler.END

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