from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Replace this with your real token
TOKEN = "7773681528:AAG2SgT_1COpScN0RBk3cLnemGv5B7kTyvk"

# Define what happens when user sends /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        ["📘 Track My Syllabus", "📆 Set Weekly Timetable"],
        ["💡 Study Tip", "💪 Motivate Me"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "👋 Hello! Welcome to Study Guide Bot!\n\nWhat would you like to do today?",
        reply_markup=markup
    )

# Create the app and add the handler
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

# Run the bot
app.run_polling()
