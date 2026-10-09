import os
import threading
from datetime import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from zoneinfo import ZoneInfo

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


# =========================
# SETTINGS
# =========================

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHANNEL_ID = os.environ.get("CHANNEL_ID", "")
CHANNEL_LINK = "https://t.me/+f05Fzq_lvMk5ZjBl"
IST = ZoneInfo("Asia/Kolkata")


# =========================
# RENDER HEALTH SERVER
# =========================

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


# =========================
# /START MESSAGE
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = """
🙏 नमस्कार!

Chiru Anand के Official Telegram Bot में आपका स्वागत है।

यहाँ आपको मिलेंगे:

📈 Stock Market Updates
📊 Market Learning & Analysis
📰 Important Financial Updates
⚠️ Risk Management Information

हमारे Private Telegram Channel को Join करने के लिए नीचे दिए गए बटन पर क्लिक करें।

⚠️ Disclaimer:
यह चैनल केवल शिक्षा और जानकारी के लिए है।
किसी भी प्रकार के Guaranteed Profit का दावा नहीं किया जाता।
निवेश करने से पहले अपने Financial Advisor की सलाह जरूर लें।
"""

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 JOIN PRIVATE CHANNEL",
                url=CHANNEL_LINK,
            )
        ],
        [
            InlineKeyboardButton(
                "✅ मैंने Join कर लिया",
                callback_data="joined",
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ About Chiru Anand",
                callback_data="about",
            )
        ],
    ]

    await update.message.reply_text(
        message,
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# =========================
# BUTTON RESPONSES
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    query = update.callback_query
    await query.answer()

    if query.data == "joined":
        await query.message.reply_text(
            """
✅ धन्यवाद!

आपने Chiru Anand Private Telegram Channel Join कर लिया है।

📈 Market को सीखें
📊 सही जानकारी समझें
⚠️ हमेशा अपना Risk Manage करें

Private Channel:
https://t.me/+f05Fzq_lvMk5ZjBl
"""
        )

    elif query.data == "about":
        await query.message.reply_text(
            """
📊 CHIRU ANAND

Stock Market Education & Awareness

✅ Market Updates
✅ Educational Content
✅ Risk Management
✅ Financial Awareness

⚠️ हम किसी भी प्रकार के Guaranteed Profit का दावा नहीं करते।
"""
        )


# =========================
# AUTOMATIC CHANNEL MESSAGE
# =========================

async def send_automatic_message(
    context: ContextTypes.DEFAULT_TYPE,
):
    if not CHANNEL_ID:
        print("CHANNEL_ID is not set")
        return

    message = """
📊 CHIRU ANAND MARKET UPDATE

बाज़ार में जल्दबाजी से नहीं, सही जानकारी और Discipline से काम करें।

✅ सही Risk Management अपनाएँ
✅ बिना Analysis के Trade न करें
✅ Stop Loss का उपयोग जरूर करें
✅ अपनी क्षमता के अनुसार ही निवेश करें

⚠️ यह संदेश केवल शिक्षा और जानकारी के लिए है।
कोई Guaranteed Profit नहीं है।
"""

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
        )
        print("Automatic channel message sent")
    except Exception as error:
        print(f"Automatic message error: {error}")


# =========================
# /TESTPOST COMMAND
# =========================

async def test_post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if not CHANNEL_ID:
        await update.message.reply_text(
            "❌ CHANNEL_ID अभी Render में सेट नहीं है।"
        )
        return

    try:
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text="""
✅ CHIRU ANAND BOT TEST

Automatic Message System Successfully चालू है।

📈 Learn
📊 Understand
⚠️ Manage Your Risk
""",
        )

        await update.message.reply_text(
            "✅ Test message channel पर भेज दिया गया।"
        )

    except Exception as error:
        await update.message.reply_text(
            f"❌ Message नहीं गया:\n{error}"
        )


# =========================
# PRIVATE CHANNEL ID DETECT
# =========================

async def detect_channel(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    if update.channel_post:
        chat_id = update.channel_post.chat.id
        print(f"PRIVATE_CHANNEL_ID={chat_id}")


# =========================
# SCHEDULE
# =========================

async def setup_jobs(application: Application):
    job_queue = application.job_queue

    schedule_times = [
        time(hour=8, minute=0, tzinfo=IST),
        time(hour=13, minute=0, tzinfo=IST),
        time(hour=18, minute=0, tzinfo=IST),
        time(hour=21, minute=30, tzinfo=IST),
    ]

    for scheduled_time in schedule_times:
        job_queue.run_daily(
            send_automatic_message,
            time=scheduled_time,
        )

    print("Automatic messages scheduled successfully")


# =========================
# MAIN BOT
# =========================

def main():
    threading.Thread(
        target=run_web_server,
        daemon=True,
    ).start()

    application = (
        Application.builder()
        .token(BOT_TOKEN)
        .post_init(setup_jobs)
        .build()
    )

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("testpost", test_post)
    )

    application.add_handler(
        CallbackQueryHandler(button_handler)
    )

    application.add_handler(
        MessageHandler(
            filters.ALL,
            detect_channel,
        ),
        group=1,
    )

    print("Chiru Anand Bot Running...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()
