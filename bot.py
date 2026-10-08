import os
import threading
from datetime import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from zoneinfo import ZoneInfo

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_LINK = "https://t.me/+f05Fzq_lvMk5ZjBl"
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")
IST = ZoneInfo("Asia/Kolkata")


# Render health server
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Chiru Anand Bot is running")

    def log_message(self, format, *args):
        return


def run_web_server():
    port = int(os.environ.get("PORT", "10000"))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    print(f"Web server running on port {port}")
    server.serve_forever()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 JOIN PRIVATE CHANNEL", url=CHANNEL_LINK)],
        [
            InlineKeyboardButton("📊 Market Learning", callback_data="learning"),
            InlineKeyboardButton("ℹ️ About", callback_data="about"),
        ],
    ]

    message = """
📊 Welcome to Chiru Anand

Get daily market learning, trading knowledge and important updates.

✅ Educational Market Updates
✅ Trading Knowledge
✅ Daily Automatic Messages
✅ Risk Management Learning

👇 Join our private Telegram channel:
"""

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "learning":
        await query.message.reply_text(
            "📚 Learn • Understand • Improve\n\n"
            "Always study the market and manage your own risk."
        )

    elif query.data == "about":
        await query.message.reply_text(
            "📊 Chiru Anand\n\n"
            "Market learning and educational trading updates.\n\n"
            "⚠️ No guaranteed profits. Trading involves risk."
        )


async def send_channel_message(context: ContextTypes.DEFAULT_TYPE):
    if not CHANNEL_ID:
        print("CHANNEL_ID is not set in Render Environment")
        return

    message = context.job.data

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            disable_web_page_preview=True,
        )
        print("Automatic message sent successfully")
    except Exception as error:
        print(f"Message sending error: {error}")


async def testpost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not CHANNEL_ID:
        await update.message.reply_text(
            "CHANNEL_ID अभी Render Environment में add नहीं है।"
        )
        return

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=(
                "✅ Chiru Anand Bot Test Successful\n\n"
                "Automatic message service is working."
            ),
        )
        await update.message.reply_text("✅ Test message channel में भेज दिया गया।")
    except Exception as error:
        await update.message.reply_text(f"❌ Error: {error}")


async def detect_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        print(f"PRIVATE_CHANNEL_ID={update.effective_chat.id}")


def schedule_messages(application: Application):
    messages = [
        (
            time(hour=8, minute=0, tzinfo=IST),
            """🌅 Good Morning Chiru Anand Family

आज का दिन discipline और सही learning के साथ शुरू करें।

📊 पहले market को समझें
🛡️ हमेशा risk manage करें
🚫 बिना research के trade न करें

⚠️ Educational purpose only.""",
            "morning",
        ),
        (
            time(hour=13, minute=0, tzinfo=IST),
            """☀️ Good Afternoon Traders

Market में patience सबसे जरूरी है।

✅ Plan के अनुसार काम करें
✅ Stop Loss का ध्यान रखें
✅ Overtrading से बचें

📊 Chiru Anand
⚠️ Trading involves risk.""",
            "afternoon",
        ),
        (
            time(hour=18, minute=0, tzinfo=IST),
            """🌆 Good Evening Chiru Anand Family

आज के market movements को review करें और अपनी गलतियों से सीखें।

📚 Learn • Understand • Improve
⚠️ No guaranteed profits.""",
            "evening",
        ),
        (
            time(hour=21, minute=30, tzinfo=IST),
            """🌙 Good Night Traders

कल के market के लिए अपना plan तैयार रखें।

✅ Capital सुरक्षित रखें
✅ Emotion control करें
✅ Risk management follow करें

📊 Chiru Anand
⚠️ Educational purpose only.""",
            "night",
        ),
    ]

    for send_time, message, name in messages:
        application.job_queue.run_daily(
            send_channel_message,
            time=send_time,
            data=message,
            name=name,
        )


def main():
    threading.Thread(target=run_web_server, daemon=True).start()

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("testpost", testpost))
    application.add_handler(button_handler := __import__(
        "telegram.ext", fromlist=["CallbackQueryHandler"]
    ).CallbackQueryHandler(button_handler))

    application.add_handler(
        MessageHandler(filters.ChatType.CHANNEL, detect_channel)
    )

    schedule_messages(application)

    print("Chiru Anand Bot Running...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
