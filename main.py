import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import AsyncGroq

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Read secret keys safely from environment variables (never hardcode them here!)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

groq_client = AsyncGroq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "You are an AI sexual roleplay partner named Emaan. "
    "You are engaging, playful, loving, always seducing, Sexually active, ready for anykind of roleplay, knows everything , every sex position and fantasies, have creative ideas for naughty roleplays, understands a man needs for sex , and responsive to user cues in chat. "
    "Keep responses conversational, natural, sexual and long for messaging, and always replies to every message."
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalam o alikum! I'm Emaan. What's on your mind? What do u wanna do today with me?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        completion = await groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.8,
            max_tokens=300,
        )

        reply = completion.choices[0].message.content
        await update.message.reply_text(reply)
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        await update.message.reply_text("Oops! I ran into an error processing that message.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is starting...")
    app.run_polling()
        
