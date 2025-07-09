import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.getenv("BOT_TOKEN", "8074365909:AAGk3CyEJQXZVeiRqPw2U-d6sYix1buwYuA")
ADMIN_USERNAME = "@CLOWNMODS"
UNLOCK_CODE = "chicken is hacked"
WEBAPP_URL = "https://chicken-road-bot.onrender.com"

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Yes", callback_data="yes_code"),
         InlineKeyboardButton("❌ No", callback_data="no_code")]
    ]
    await update.message.reply_text(
        "🐔 Welcome to our private bot!\n\n✨ Stylish hacks. Trusted signals. Secure access only.\n\n"
        "🔐 Do you have your secret code to unlock the bot?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Handle Yes/No buttons
async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "yes_code":
        await query.edit_message_text("🔐 Enter your access code to unlock the bot.\n\n(Just type it below)")
    elif query.data == "no_code":
        await query.edit_message_text(f"💸 You can buy your access code from admin:\n👉 {ADMIN_USERNAME}")

# Handle user code input
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()

    if text == UNLOCK_CODE.lower():
        keyboard = [[InlineKeyboardButton("🚀 Get Signal", web_app=WebAppInfo(url=WEBAPP_URL))]]
        await update.message.reply_text("✅ Code accepted! Tap below to open WebApp.",
                                        reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(f"❌ Invalid code. Contact admin: {ADMIN_USERNAME}")

# Main entry
if __name__ == '__main__':
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot started.")
    app.run_polling()
