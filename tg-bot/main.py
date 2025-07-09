import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
)
import httpx
from config import BOT_TOKEN, BACKEND_HOST, MINIAPP_HOST

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RU = "ru"
EN = "en"

def get_language(update: Update) -> str:
    if update.effective_user and update.effective_user.language_code == RU:
        return RU
    return EN

def get_miniapp_url(path: str) -> str:
    return f"{MINIAPP_HOST}{path}"

async def is_registered(user_id: int) -> bool:
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(f"{BACKEND_HOST}/user/isRegistered/{user_id}")
            return resp.status_code == 200 and resp.json() is True
        except Exception as e:
            logger.error(f"Backend error: {e}")
            return False

def get_start_text(lang):
    return {
        RU: "Привет! Я Mealix Bot! Вы можете приступить к настройкам в мини-апп",
        EN: "Hello! I'm Mealix Bot! You can start the settings in the mini-app"
    }[lang]

def get_settings_text(lang):
    return {
        RU: "Вы можете приступить к настройкам в мини-апп",
        EN: "You can start the settings in the mini-app"
    }[lang]

def get_button_text(lang):
    return {
        RU: "Мини-апп",
        EN: "Mini-app"
    }[lang]

def get_already_registered_text(lang):
    return {
        RU: "Вы уже зарегистрированы",
        EN: "You are already registered"
    }[lang]

def get_error_text(lang):
    return {
        RU: "Что-то пошло не так с обработкой обновления",
        EN: "Something went wrong with the update handling"
    }[lang]

def miniapp_keyboard(path, lang):
    url = get_miniapp_url(path)
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(get_button_text(lang), url=url)]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_language(update)
    if await is_registered(user_id):
        await update.message.reply_text(get_already_registered_text(lang))
    else:
        await update.message.reply_text(
            get_start_text(lang),
            reply_markup=miniapp_keyboard(f"/newuser?user_id={user_id}", lang)
        )

async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_language(update)
    if not await is_registered(user_id):
        await update.message.reply_text(get_start_text(lang),
            reply_markup=miniapp_keyboard(f"/newuser?user_id={user_id}", lang)
        )
    else:
        await update.message.reply_text(
            get_settings_text(lang),
            reply_markup=miniapp_keyboard(f"/settings?user_id={user_id}", lang)
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_language(update)
    text = update.message.text
    if text == "/start":
        await start(update, context)
        return
    if text == "/settings":
        await settings(update, context)
        return
    if await is_registered(user_id):
        await update.message.reply_text(get_error_text(lang))
    else:
        await update.message.reply_text(get_start_text(lang),
            reply_markup=miniapp_keyboard(f"/newuser?user_id={user_id}", lang)
        )

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main() 