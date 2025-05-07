from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import logging

# --- CONFIGURATION ---
TOKEN = '8155849903:AAEXuuAvVK_SzoRhPufTFjbbkSMjAtL1UNA'
CHANNEL_USERNAME = '@seconddatememe'  # Make sure bot is an admin here
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
        'type_message': '📝 لطفاً پیامت را بنویس یا ویس بفرست.',
        'sent': '✅ پیامت ناشناس ارسال شد!',
        'rules': """🚫قوانین ربات اعترافات ناشناس🚫
(لطفاً بخون تا دور هم خوش بگذره نه دل بشکنه) :)

1⃣ اطلاعات شخصی دیگران رو فاش نکن.
اسم، آدرس، شماره، شماره دمپایی! هر چی که بشه کسی رو شناسایی کرد، ممنوعه

2⃣ تبلیغات ممنوعه.
(همکاری فقط پیوی ادمین)

3⃣ شوخی با مسائل خاص (مذهب، قومیت، جنسیت و...) ممنوع.
بخندیم، ولی به قیمت دل کسی نباشه

4⃣ حق انتشار با ادمینه.
ممکنه بعضی اعترافا که خلاف قوانین هستن منتشر نشن، لطفاً دلخور نشو

5⃣ مسئولیت حرفات با خودته.
ما فقط یه دونه جعبه خاطراتیم

6⃣ توهین، فحش، یا تمسخر ممنوعه.
اینجا جاییه برای خالی‌کردن دل، نه خالی‌کردن عقده!

7⃣ اعترافات نباید شامل خشونت، تهدید، یا آسیب به دیگران باشه

✅قوانین شامل همه افراد میشه و امیدواریم محیط شاد و امنی کنار هم داشته باشیم""",
        'talk_to_admin': '📝 پیامت را بنویس، ادمین به زودی پاسخ خواهد داد.'
    },
    'en': {
        'welcome': "Oh! You came to confess? 😁 Welcome!\n\nWelcome to the Second Date club, buddy 😊",
        'menu': [
            '📤 Send an anonymous message',
            '👤 Talk to admin',
            '💡 Suggestions',
            '📜 Rules',
            '❓ Help'
        ],
        'type_message': '📝 Please type your message or record a voice message and send it.',
        'sent': '✅ Your message was sent anonymously!',
        'rules': """🚫 Anonymous Confession Bot Rules 🚫
(Please read, so we all have fun without hurting anyone) :)

1⃣ Do not share personal information of others.
Names, addresses, phone numbers, even shoe sizes — anything that identifies someone is forbidden.

2⃣ Advertising is prohibited.
(Contact admin privately for collaborations.)

3⃣ No jokes about sensitive topics (religion, ethnicity, gender, etc.).
Let's laugh together, but not at the expense of others.

4⃣ Admin has the right to publish or reject confessions.
Some may not be posted if they break the rules — please understand.

5⃣ You are responsible for your own words.
We are just a memory box.

6⃣ No insults, profanity, or mocking others.
This is a place to share your feelings, not your grudges!

7⃣ Confessions must not include violence, threats, or harm to others.

✅ Rules apply to everyone. Let's create a happy and safe space together.""",
        'talk_to_admin': '📝 Leave your message and the admin will reply shortly.'
    }
}

# --- USER STATES ---
user_lang = {}
waiting_for_message = {}
waiting_for_admin = {}

# --- HANDLERS ---
async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    keyboard = [[
        InlineKeyboardButton("فارسی", callback_data='lang_fa'),
        InlineKeyboardButton("English", callback_data='lang_en')
    ]]
    await update.message.reply_text(
        "Please choose your language:\nلطفاً زبان خود را انتخاب کنید:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def language_selection(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    lang_code = query.data.split('_')[1]
    user_id = query.from_user.id
    user_lang[user_id] = lang_code

    lang = LANGUAGES[lang_code]

    # Check channel membership
    member = await context.bot.get_chat_member(CHANNEL_USERNAME, user_id)
    if member.status in ['member', 'creator', 'administrator']:
        keyboard = [[KeyboardButton(opt)] for opt in lang['menu']]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        await query.message.reply_text(lang['welcome'], reply_markup=reply_markup)
    else:
        await query.message.reply_text("You must join our channel first: " + CHANNEL_USERNAME)

async def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = user.id

    lang_code = user_lang.get(user_id, 'en')
    text = update.message.text if update.message.text else ''
    voice = update.message.voice if update.message.voice else None

    # Handle buttons first
    if text == LANGUAGES[lang_code]['menu'][0]:  # 📤 Send an anonymous message
        waiting_for_message[user_id] = True
        waiting_for_admin.pop(user_id, None)
        await update.message.reply_text(LANGUAGES[lang_code]['type_message'])
        return

    if text == LANGUAGES[lang_code]['menu'][1]:  # 👤 Talk to admin
        waiting_for_admin[user_id] = True
        waiting_for_message.pop(user_id, None)
        await update.message.reply_text(LANGUAGES[lang_code]['talk_to_admin'])
        return

    if text == LANGUAGES[lang_code]['menu'][3]:  # 📜 Rules
        await update.message.reply_text(LANGUAGES[lang_code]['rules'])
        return

    # Now check if they are sending a message after clicking a button
    if waiting_for_message.get(user_id):
        sender_info = f"👤 New anonymous message:\n"
        sender_info += f"Name: {user.full_name}\n"
        sender_info += f"Username: @{user.username if user.username else 'No username'}\n"
        sender_info += f"User ID: {user_id}\n\n"

        for admin_id in ADMINS:
            if text:
                await context.bot.send_message(chat_id=admin_id, text=sender_info + text)
            if voice:
                await context.bot.send_message(chat_id=admin_id, text=sender_info)
                await context.bot.send_voice(chat_id=admin_id, voice=voice.file_id)

        await update.message.reply_text(LANGUAGES[lang_code]['sent'])
        waiting_for_message.pop(user_id)

    elif waiting_for_admin.get(user_id):
        sender_info = f"👤 Message to Admin:\n"
        sender_info += f"Name: {user.full_name}\n"
        sender_info += f"Username: @{user.username if user.username else 'No username'}\n"
        sender_info += f"User ID: {user_id}\n\n"

        for admin_id in ADMINS:
            if text:
                await context.bot.send_message(chat_id=admin_id, text=sender_info + text)
            if voice:
                await context.bot.send_message(chat_id=admin_id, text=sender_info)
                await context.bot.send_voice(chat_id=admin_id, voice=voice.file_id)

        await update.message.reply_text("✅ Your message was sent to the admin.")
        waiting_for_admin.pop(user_id)

    else:
        await update.message.reply_text("❓ Please select an option from the menu.")

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
app.add_handler(CallbackQueryHandler(language_selection))
app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, handle_message))

app.run_polling()
