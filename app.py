"""
bot/bot.py — بوت تيليجرام
python-telegram-bot v20
تشغيل: python bot.py
"""
import os
import threading
from dotenv import load_dotenv
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN    = os.environ.get('BOT_TOKEN',    'YOUR_BOT_TOKEN_HERE')
WEBAPP_URL   = os.environ.get('WEBAPP_URL',   'https://waredwebsite2.vercel.app/')
ADMIN_ID     = int(os.environ.get('ADMIN_ID', '8988236075'))
CHANNEL_URL  = os.environ.get('CHANNEL_URL',  'https://t.me/medo_channel')
SUPPORT_URL  = os.environ.get('SUPPORT_URL',  'https://t.me/medo_add')
FLASK_HOST   = os.environ.get('FLASK_HOST', '0.0.0.0')
FLASK_PORT   = int(os.environ.get('FLASK_PORT', '5002'))

flask_app = Flask(__name__)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    args = ctx.args or []
    ref  = args[0].replace('ref_', '') if args and args[0].startswith('ref_') else ''
    url  = f"{WEBAPP_URL}?tg=1&ref={ref}" if ref else f"{WEBAPP_URL}?tg=1"

    kb = [
        [InlineKeyboardButton("🚀 افتح التطبيق", web_app=WebAppInfo(url=url))],
        [InlineKeyboardButton("📢 قناتنا", url=CHANNEL_URL),
         InlineKeyboardButton("🆘 الدعم",  url=SUPPORT_URL)]
    ]
    await update.message.reply_text(
        f"👋 أهلاً *{user.first_name}*!\n\n"
        "⚡ *Reward Ads* — اكسب من مشاهدة الإعلانات\n\n"
        "📺 شاهد إعلانات واكسب مكافآت فورية\n"
        "👥 ادعُ أصدقاءك واحصل على عمولة *5%*\n"
        "💳 اسحب أرباحك عبر محافظ الدفع الإلكتروني\n\n"
        "👇 اضغط لفتح التطبيق الآن!",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🚀 افتح التطبيق", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("📢 القناة", url=CHANNEL_URL),
         InlineKeyboardButton("🆘 الدعم",  url=SUPPORT_URL)]
    ]
    await update.message.reply_text(
        "📋 *كيفية الاستخدام:*\n\n"
        "1️⃣ افتح التطبيق\n"
        "2️⃣ اضغط 'شاهد إعلان' وانتظر العداد\n"
        "3️⃣ تُضاف المكافأة لرصيدك تلقائياً\n"
        "4️⃣ شارك رابط الإحالة واكسب 5%\n"
        "5️⃣ اسحب عند وصول رصيدك للحد الأدنى",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def admin_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ غير مصرح لك")
        return
    admin_url = WEBAPP_URL.replace(':5000', ':5001').rstrip('/') + '/'
    kb = [[InlineKeyboardButton("⚙️ لوحة التحكم", url=admin_url)]]
    await update.message.reply_text("🛡️ *لوحة الأدمن*", parse_mode='Markdown',
                                    reply_markup=InlineKeyboardMarkup(kb))


@flask_app.route('/')
def index():
    return '<h1>Flask server is running</h1><p>Welcome to Reward Ads bot server.</p>'


def run_flask():
    print(f"🌐 Flask running on http://{FLASK_HOST}:{FLASK_PORT}")
    flask_app.run(host=FLASK_HOST, port=FLASK_PORT)


def run_bot():
    bot_app = Application.builder().token(BOT_TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("help",  help_cmd))
    bot_app.add_handler(CommandHandler("admin", admin_cmd))
    print("🤖 Bot running...")
    bot_app.run_polling(allowed_updates=Update.ALL_TYPES)


def main():
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    bot_thread = threading.Thread(target=run_bot, daemon=True)

    flask_thread.start()
    bot_thread.start()

    flask_thread.join()
    bot_thread.join()


if __name__ == '__main__':
    main()
