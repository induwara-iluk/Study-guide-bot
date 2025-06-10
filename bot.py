import json
import random
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from ask_bot import ask_ugc_bot  # Your existing UGC assistant

# Load tips and motivations
with open("assets/study_tips.json", "r") as f:
    study_tips = json.load(f)

with open("assets/motivations.json", "r") as f:
    motivations = json.load(f)

# Bot token
TOKEN = "7773681528:AAG2SgT_1COpScN0RBk3cLnemGv5B7kTyvk"

# Global flag to track chat mode
user_chat_mode = {}

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_keyboard = [
        
        ["💡 Study Tip", "💪 Motivate Me"],
        ["💬 Chat with Study Advisor"]
    ]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Hello! Welcome to Study Guide Bot!\n\nWhat would you like to do today?",
        reply_markup=markup
    )
    user_chat_mode[update.effective_chat.id] = False

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    chat_id = update.effective_chat.id

    # Exit chat mode
    if user_input == "🔚 Exit Chat Mode":
        user_chat_mode[chat_id] = False
        reply_keyboard = [
            ["💡 Study Tip", "💪 Motivate Me"],
            ["💬 Chat with Study Advisor"]
        ]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        await update.message.reply_text("✅ You have exited chat mode.", reply_markup=markup)
        return

    # If user enters chat mode
    if user_input == "💬 Chat with Study Advisor":
        user_chat_mode[chat_id] = True
        reply_keyboard = [["🔚 Exit Chat Mode"]]
        markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True)
        await update.message.reply_text(
            "🧠 Great! Ask me anything about university admissions in Sri Lanka.",
            reply_markup=markup
        )
        return

    # If in chat mode, answer the question
    if user_chat_mode.get(chat_id, False):
        try:
            response = ask_ugc_bot(user_input)
            await update.message.reply_text(response)
        except Exception as e:
            await update.message.reply_text("⚠️ Sorry, something went wrong while answering your question.")
        return

    # Study Tip
    if user_input == "💡 Study Tip":
        tip = random.choice(study_tips)
        await update.message.reply_text(f"💡 Study Tip:\n{tip}")
        return

    # Motivation
    if user_input == "💪 Motivate Me":
        motivation = random.choice(motivations)
        await update.message.reply_text(f"🔥 Motivation:\n{motivation}")
        return

    # Default
    await update.message.reply_text("👉 Please use one of the options in the keyboard.")

# Set up bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
