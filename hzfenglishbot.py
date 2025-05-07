from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import logging

# --- CONFIGURATION ---
TOKEN = '8155849903:AAHE82n70YOiTJIFQCW2BQBYTUKdmNWW0GY'
CHANNEL_USERNAME = '@seconddatememe'  # Bot must be admin here
ADMINS = [147545489, 1255179632]  # Replace with your Telegram user ID(s)

# --- LOGGING ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- LANGUAGES ---
LANGUAGES = {
    'fa': {
        'welcome': 'عه! اومدی اعتراف کنی😁 خوش اومدی\n\nبه جمع سکند دیت خوش اومدی رفیق 😊',
        'menu': [
            '📤 ارسال پیام ناشناس',
            '👤 صحبت با ادمین',
            '💡 پیشنهادات',
            '📜 قوانین',
            '❓ راهنما'
        ],
        'rules': '🚫قوانین ربات اعترافات ناشناس🚫\n (لطفاً بخون تا دور هم خوش بگذره نه دل بشکنه) :)\n\n1⃣ اطلاعات شخصی دیگران رو فاش نکن.\nاسم، آدرس، شماره، شماره دمپایی! هر چی که بشه کسی رو شناسایی کرد، ممنوعه\n\n2⃣تبلیغات ممنوعه. (همکاری فقط پیوی ادمین)\n\n3⃣ شوخی با مسائل خاص (مذهب، قومیت، جنسیت و...) ممنوع.\nبخندیم، ولی به قیمت دل کسی نباشه\n\n4⃣حق انتشار با ادمینه. ممکنه بعضی اعترافا که خلاف قوانین هستن منتشر نشن، لطفاً دلخور نشو\n\n5⃣مسئولیت حرفات با خودته. ما فقط یه دونه جعبه خاطراتیم\n\n6⃣توهین، فحش، یا تمسخر ممنوعه.\nاینجا جاییه برای خالی‌کردن دل، نه خالی‌کردن عقده!\n\n7⃣اعترافات نباید شامل خشونت، تهدید، یا اسیب به دیگران باشه\n\n✅قوانین شامل همه افراد میشه و امیدواریم محیط شاد و امنی کنار هم داشته باشیم',
        'rules_en': "🚫 Anonymous Confession Bot Rules 🚫\n(Please read to keep it fun and kind!) :)\n\n1⃣ Do not share others' personal information.\nName, address, phone number, even slipper size! Anything that could reveal someone's identity is forbidden.\n\n2⃣ No advertising. (Collaborations only via admin's private chat.)\n\n3⃣ No jokes about sensitive topics (religion, ethnicity, gender, etc.)\nLet's laugh, but not at someone's expense.\n\n4⃣ Admin decides what gets posted.\nSome confessions may not be posted if they break rules, please understand.\n\n5⃣ You're responsible for your words.\nWe're just a memory box!\n\n6⃣ No insults, curses, or mocking.\nThis is a place to lighten hearts, not to spread negativity.\n\n7⃣ Confessions must not include violence, threats, or harm to others.\n\n✅ Rules apply to everyone. Let's keep it fun and safe together!",
        'admin_prompt': '📝 پیامت را بنویس و به همراه آیدی ارسال کن، ادمین به زودی پاسخ خواهد داد.',
        'suggestion_prompt': 'نظر پیشنهاد یا انتقادت رو اینجا بنویس و ارسال کن📪',
'guide': '📜چیز خاصی نیس فقط بزن روی ارسال پیام، پیامتو بنویس یا ویس بگیر بعدشم بفرست، پیامت ناشناس میره واسه ادمین و ادمین انلی🧧\n🥷ادمین تن صدارو تغییر میده و بصورت ناشناس پست میکنه\n✅بقیه دوستان هم میان نظر میدن همین'
    },
}

# --- USER STATE ---
user_lang = {}
user_state = {}

# --- STATES ---
STATE_ANON = 'anonymous'
STATE_ADMIN = 'admin'
STATE_SUGGESTION = 'suggestion'

# --- HANDLERS ---
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    user_lang[user_id] = 'fa'
    lang = LANGUAGES['fa']

    # Check channel membership
    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
    if member.status in ['member', 'creator', 'administrator']:
        keyboard = [[KeyboardButton(opt)] for opt in lang['menu']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await update.message.reply_text(lang['welcome'], reply_markup=reply_markup)
    else:
        await update.message.reply_text(f"❗️برای استفاده از ربات، اول عضو کانال شو 👈🏻 {CHANNEL_USERNAME}\n✅ عضو شدی روی این گزینه بزن 👈🏻 /start")



async def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    lang_code = user_lang.get(user_id, 'en')
    text = update.message.text
    state = user_state.get(user_id)

    # ✅ Membership check added here
    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
    if member.status not in ['member', 'creator', 'administrator']:
        await update.message.reply_text(f"❗️برای استفاده از ربات، اول عضو کانال شو 👈🏻 {CHANNEL_USERNAME}\n✅ عضو شدی روی این گزینه بزن 👈🏻 /start")

        return

    if text in LANGUAGES[lang_code]['menu']:
        if text.startswith('📤'):
            user_state[user_id] = STATE_ANON
            await update.message.reply_text("خاطره‌ات رو ویس بگیر و بفرست، \n (ادمین صداتو تغییر میده که ناشناس بمونی)👌🏻\nاگه خجالت می‌کشی تایپش کن 👍🏻\n حواست باشه یدونه پیام باشه!\n خواستی میتونی یه لقب با هشتگ واسه خودت بذاری :))")
        elif text.startswith('👤'):
            user_state[user_id] = STATE_ADMIN
            await update.message.reply_text(LANGUAGES[lang_code]['admin_prompt'])
        elif text.startswith('💡'):
            user_state[user_id] = STATE_SUGGESTION
            await update.message.reply_text(LANGUAGES[lang_code]['suggestion_prompt'])
        elif text.startswith('📜'):
            await update.message.reply_text(LANGUAGES[lang_code]['rules'])
        elif text.startswith('❓'):
            await update.message.reply_text(LANGUAGES[lang_code]['guide'])
        return

    if state == STATE_ANON:
        for admin_id in ADMINS:
            msg = f"\U0001F464 Anonymous Message\nName: {update.effective_user.first_name or ''} {update.effective_user.last_name or ''}\nUsername: @{update.effective_user.username or 'None'}\nUserID: {user_id}\n\nMessage:\n{text}"
            await context.bot.send_message(chat_id=admin_id, text=msg)
        await update.message.reply_text("✅ پیام ناشناس شما ارسال شد!")
    elif state == STATE_ADMIN:
        for admin_id in ADMINS:
            msg = f"\U0001F4E8 Message to Admin\nName: {update.effective_user.first_name or ''} {update.effective_user.last_name or ''}\nUsername: @{update.effective_user.username or 'None'}\nUserID: {user_id}\n\nMessage:\n{text}"
            await context.bot.send_message(chat_id=admin_id, text=msg)
        await update.message.reply_text("✅ پیام شما برای ادمین ارسال شد!")
    elif state == STATE_SUGGESTION:
        for admin_id in ADMINS:
            msg = f"\U0001F4AC Suggestion\nName: {update.effective_user.first_name or ''} {update.effective_user.last_name or ''}\nUsername: @{update.effective_user.username or 'None'}\nUserID: {user_id}\n\nMessage:\n{text}"
            await context.bot.send_message(chat_id=admin_id, text=msg)
        await update.message.reply_text("✅ پیشنهاد شما ارسال شد!")

    user_state.pop(user_id, None)


async def reply_to_user(update: Update, context: CallbackContext):
    if update.effective_user.id not in ADMINS:
        return

    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Usage: /reply <user_id> <message>")
        return

    user_id = int(args[0])
    message_text = ' '.join(args[1:])
    await context.bot.send_message(chat_id=user_id, text=f"The ADMIN says: {message_text}")
    await update.message.reply_text("✅ Reply sent anonymously.")

# --- MAIN ---
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('reply', reply_to_user))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

app.run_polling()
