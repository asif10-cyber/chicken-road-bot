import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

BOT_TOKEN = os.getenv("BOT_TOKEN", "8074365909:AAGk3CyEJQXZVeiRqPw2U-d6sYix1buwYuA")
WEBAPP_URL = "https://chicken-road-bot.onrender.com/static/chicken.html"
ADMIN_USERNAME = "@CLOWNMODS"
UNLOCK_CODE = "chicken is hacked"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Get Signal", callback_data="get_signal")],
    ]
    await update.message.reply_text(
        "👋 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗖𝗛𝗜𝗖𝗞𝗘𝗡 𝗥𝗢𝗔𝗗 𝗕𝗢𝗧\n\n🔐 Enter your access code to unlock the bot.\nIf you don't have a code, message our admin " + ADMIN_USERNAME,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "get_signal":
        user_id = query.from_user.id
        if user_data.get(user_id) == UNLOCK_CODE:
            await query.message.reply_text("🚀 Opening Signal Panel...", reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🟡 Open WebApp", web_app=WebAppInfo(url=WEBAPP_URL))]
            ]))
        else:
            await query.message.reply_text("❌ You need to enter a valid code first.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if text == UNLOCK_CODE:
        user_data[update.message.from_user.id] = UNLOCK_CODE
        await update.message.reply_text("✅ Code accepted! Tap below to open WebApp.", reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🟡 Open WebApp", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]))
    else:
        await update.message.reply_text("❌ Invalid code. Contact admin: " + ADMIN_USERNAME)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
