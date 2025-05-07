from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import logging

# --- CONFIGURATION ---
TOKEN = '8155849903:AAHE82n70YOiTJIFQCW2BQBYTUKdmNWW0GY'  # Replace with your actual bot token
CHANNEL_USERNAME = '@seconddatememe'  # Bot must be admin here
ADMINS = [147545489, 1255179632]  # Replace with your Telegram user ID(s)

# --- LOGGING ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- LANGUAGE ---
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
        'admin_prompt': '📝 پیامت را بنویس و به همراه آیدی ارسال کن، ادمین به زودی پاسخ خواهد داد.',
        'suggestion_prompt': 'نظر، پیشنهاد یا انتقادت رو اینجا بنویس و ارسال کن📪',
        'guide': '📜چیز خاصی نیس فقط بزن روی ارسال پیام، پیامتو بنویس یا ویس بگیر بعدشم بفرست، پیامت ناشناس میره واسه ادمین و ادمین انلی🧧\n🥷ادمین تن صدارو تغییر میده و بصورت ناشناس پست میکنه\n✅بقیه دوستان هم میان نظر میدن همین'
    }
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
        await update.message.reply_text("❗️برای استفاده از ربات، اول عضو کانال شو 👈🏻 " + CHANNEL_USERNAME)
        return

    # ✅ Only proceed if user selected something from the menu
    if text in LANGUAGES[lang_code]['menu']:
        if text.startswith('📤'):
            user_state[user_id] = STATE_ANON
            await update.message.reply_text(
                "خاطره‌ات رو ویس بگیر و بفرست، \n"
                "(ادمین صداتو تغییر میده که ناشناس بمونی)👌🏻\n"
                "اگه خجالت می‌کشی تایپش کن 👍🏻\n"
                "حواست باشه یدونه پیام باشه!\n"
                "خواستی می‌تونی یه لقب با هشتگ واسه خودت بذاری :))"
            )
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

    # ✅ If user sends message without selecting an action, ignore
    if state is None:
        await update.message.reply_text("لطفاً یکی از گزینه‌های منو رو انتخاب کن 😊")
        return

    # ✅ Handle based on state
    if state == STATE_ANON:
        for admin_id in ADMINS:
            msg = f"\U0001F464 پیام ناشناس\nName: {update.effective_user.first_name or ''} {update.effective_user.last_name or ''}\nUsername: @{update.effective_user.username or 'None'}\nUserID: {user_id}\n\nMessage:\n{text}"
            await context.bot.send_message(chat_id=admin_id, text=msg)
        await update.message.reply_text("✅ پیام ناشناس شما ارسال شد!")
    elif state == STATE_ADMIN:
        for admin_id in ADMINS:
            msg = f"\U0001F4E8 پیام برای ادمین\nName: {update.effective_user.first_name or ''} {update.effective_user.last_name or ''}\nUsername: @{update.effective_user.username or 'None'}\nUserID: {user_id}\n\nMessage:\n{text}"
            await context.bot.send_message(chat_id=admin_id, text=msg)
        await update.message.reply_text("✅ پیام شما برای ادمین ارسال شد!")
    elif state == STATE_SUGGESTION:
        for admin_id in ADMINS:
            msg = f"\U0001F4AC پیشنهاد\nName: {update.effective_user.first_name or ''} {update.effective_user.last_name or ''}\nUsername: @{update.effective_user.username or 'None'}\nUserID: {user_id}\n\nMessage:\n{text}"
            await context.bot.send_message(chat_id=admin_id, text=msg)
        await update.message.reply_text("✅ پیشنهاد شما ارسال شد!")

    user_state.pop(user_id, None)

