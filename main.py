"""
MUOMILA Telegram Bot
====================
- ReplyKeyboardMarkup  → klaviatura ekran pastida (professional)
- WebApp "Ilova" tugma → klaviaturaning chap tepasida Mini App ochadi
- InlineKeyboard       → faqat kontentda (qo'llanma, FAQ, obuna)
- Async + polling      → bir vaqtda 1000+ foydalanuvchi ishlata oladi
- python-telegram-bot  v20+
"""
from telegram.ext import ApplicationBuilder
import asyncio
import logging

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

# ─────────────────────────────────────────────────────────────
#  SOZLAMALAR  ← faqat BOT_TOKEN ni o'zgartiring
# ─────────────────────────────────────────────────────────────
BOT_TOKEN      = "8536529672:AAGTgi5iAU9EGNQzhA8srM-CEEqlKLJ726E"   # @BotFather dan olingan token
ADMIN_USERNAME = "@Padiwakh_1"
ADMIN_PHONE    = "+998 91 167 29 20"
ADMIN_EMAIL    = "saidmaxmudovrahmonsaid@gmail.com"
APP_URL        = "https://muomila.onrender.com/login.html#debtors"

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ═════════════════════════════════════════════════════════════
#  REPLY KLAVIATURA  (ekran pastida — har doim ko'rinadi)
# ═════════════════════════════════════════════════════════════

def main_reply_kb():
    """
    Klaviatura:
      [ 🌐 Ilova ]  ← WebApp Mini App tugmasi (chap tepada)
      [ ℹ️ Biz haqimizda ]  [ 💳 Obuna ]
      [ 📖 Qo'llanma ]      [ 🆘 Yordam ]
    """
    return ReplyKeyboardMarkup(
        [
            # 1-qator: WebApp tugmasi — klaviaturaning chap tepasida
            [KeyboardButton("🌐  Ilova", web_app=WebAppInfo(url=APP_URL))],
            # 2-qator
            [
                KeyboardButton("ℹ️  Biz haqimizda"),
                KeyboardButton("💳  Obuna sotib olish"),
            ],
            # 3-qator
            [
                KeyboardButton("📖  Qo'llanma"),
                KeyboardButton("🆘  Yordam"),
            ],
        ],
        resize_keyboard=True,       # klaviatura kichikroq — chiroyli
        is_persistent=True,         # klaviatura doim ko'rinadi
    )


# ═════════════════════════════════════════════════════════════
#  INLINE KLAVIATURALAR
# ═════════════════════════════════════════════════════════════

def guide_inline_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📝  Qarz qo'shish",    callback_data="g_debt")],
        [InlineKeyboardButton("🏢  Firma bo'limi",     callback_data="g_firma")],
        [InlineKeyboardButton("📊  Statistika",        callback_data="g_stats")],
        [InlineKeyboardButton("🔔  Eslatmalar",        callback_data="g_notif")],
        [InlineKeyboardButton("🔒  Xavfsizlik",        callback_data="g_sec")],
    ])

def help_inline_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("❓  Ko'p so'raladigan savollar", callback_data="faq")],
        [InlineKeyboardButton("📞  Admin bilan bog'lanish",     callback_data="contact")],
    ])

def faq_inline_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔐  Kirish / Ro'yxat",  callback_data="fq_login")],
        [InlineKeyboardButton("💰  Obuna & To'lov",     callback_data="fq_pay")],
        [InlineKeyboardButton("📝  Qarz boshqarish",    callback_data="fq_debt")],
        [InlineKeyboardButton("📊  Statistika & PDF",   callback_data="fq_stats")],
        [InlineKeyboardButton("📱  Texnik savollar",    callback_data="fq_tech")],
        [InlineKeyboardButton("◀️  Orqaga",             callback_data="back_help")],
    ])

def back_guide_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️  Qo'llanmaga qaytish", callback_data="back_guide")]
    ])

def back_faq_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("◀️  FAQ ga qaytish", callback_data="faq")]
    ])

def sub_inline_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬  Adminga yozish", url="https://t.me/Padiwakh_1")],
    ])

def contact_inline_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬  Telegramda yozish", url="https://t.me/Padiwakh_1")],
        [InlineKeyboardButton("◀️  Yordamga qaytish",  callback_data="back_help")],
    ])


# ═════════════════════════════════════════════════════════════
#  MATNLAR
# ═════════════════════════════════════════════════════════════

ABOUT_TEXT = """🏦 <b>MUOMILA — Qarz va Kelishuvlarni Ishonchli Boshqarish</b>

MUOMILA — oddiy odamlar, do'konlar va firmalar o'rtasidagi qarz munosabatlarini <b>rasmiylashtirish</b>, <b>nazorat qilish</b> va <b>isbot bilan saqlash</b> uchun yaratilgan zamonaviy raqamli platforma.

Endi <i>"qarz olmaganman"</i>, <i>"esimdan chiqibdi"</i> kabi muammolar bo'lmaydi — <b>hammasi yozma, sana bilan va isbot bilan saqlanadi.</b>

━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>Maqsad</b>
Moliyaviy ishonchni mustahkamlash, qarz jarayonini shaffof va nazorat qilinadigan tizimga aylantirish.

━━━━━━━━━━━━━━━━━━━━━━
🔑 <b>Asosiy imkoniyatlar</b>
✍️ Raqamli qarz shartnomasi — imzo bilan
💰 Pul yoki mahsulot qarzini yozish
👥 Jismoniy shaxslar, do'konlar, firmalar uchun
📄 PDF / DOCX shartnoma (isbot hujjati)
🔔 Avtomatik eslatmalar — muddat yaqinlashganda
📊 Statistika paneli — jami, to'langan, qoldiq
☁️ Bulutda saqlash — ma'lumotlar yo'qolmaydi
🔐 Kuchli shifrlash va xavfsizlik
🌙 Dark / Light mode
📱 Android, iOS va Web

━━━━━━━━━━━━━━━━━━━━━━
💼 <b>Kimlar uchun</b>
• Do'st, tanish, qarindosh bilan qarz
• Do'kon va savdo egalari
• Kichik biznes va firmalar
• Qarz bilan ishlaydigan har qanday shaxs

━━━━━━━━━━━━━━━━━━━━━━
🚀 <b>Afzalliklar</b>
• Yozma va isbotli qarz shartnomasi
• Inkor qilish yoki esdan chiqarish yo'q
• Barcha qarzlar bitta joyda
• Qog'ozsiz raqamli tizim
• Huquqiy dalil sifatida ishlatish mumkin"""

SUBSCRIPTION_TEXT = f"""💳 <b>MUOMILA Obuna Rejalari</b>

Obuna sotib olish uchun <b>admin bilan bog'laning</b>:

👤 <b>Saidmaxmudov Rahmonsaid</b>
📞 {ADMIN_PHONE}
💬 {ADMIN_USERNAME}
📧 {ADMIN_EMAIL}

━━━━━━━━━━━━━━━━━━━━━━
📦 <b>Rejalar</b>

🗓 <b>1 Oylik — 50,000 so'm</b>
  ✅ Barcha funksiyalar · 24/7 qo'llab-quvvat
  ✅ Cheksiz qarzlar · Statistika · PDF

⭐ <b>3 Oylik — 135,000 so'm</b> <i>(oyiga 45,000)</i>
  ✅ 15% chegirma · Premium qo'llash · PDF

💎 <b>6 Oylik — 250,000 so'm</b> <i>(oyiga 41,667)</i>
  ✅ 28% chegirma · VIP qo'llab-quvvat
  ✅ Avtomatik eslatmalar · PDF

👑 <b>12 Oylik — 450,000 so'm</b> <i>(oyiga 37,500)</i>
  ✅ 35% chegirma · Barcha yangilanishlar
  ✅ Ekstra imkoniyatlar · PDF

━━━━━━━━━━━━━━━━━━━━━━
⏰ Ish vaqti: <b>Har kuni 09:00–21:00</b>"""

GUIDE_TEXT = """📖 <b>Qo'llanma — bo'lim tanlang</b>

📝 Qarz qo'shish tartibi
🏢 Firma bo'limi (Hamkor)
📊 Statistika va hisobotlar
🔔 Eslatmalar
🔒 Xavfsizlik va maxfiylik"""

GUIDE_DEBT = f"""📝 <b>Qarz qo'shish — bosqichma-bosqich</b>

<b>1.</b> Ilova tugmasini bosib oching 👉 yoki:
    <a href="{APP_URL}">muomila.onrender.com</a>

<b>2.</b> Pastki menyudan <b>Qarzdorlar</b> bo'limini oching

<b>3.</b> <b>"Qarz qo'shish"</b> tugmasini bosing

<b>4.</b> Ma'lumotlarni to'ldiring:
   • Ism Familiya <i>(majburiy)</i>
   • Telefon raqami <i>(majburiy)</i>
   • Qarz summasi so'mda <i>(majburiy)</i>
   • Qaytarish sanasi <i>(majburiy)</i>
   • Izoh / tavsif <i>(ixtiyoriy)</i>
   • Rasm — chek yoki dalil <i>(ixtiyoriy)</i>

<b>5.</b> ✍️ Imzo chizing — <b>majburiy</b> (qonuniy tasdiqlash)

<b>6.</b> <b>Saqlash</b> tugmasini bosing ✅

━━━━━━━━━━━━━━━━━━━━━━
💡 Bepul rejimda <b>5 tagacha</b> qarz.
Cheksiz qarz uchun — obuna sotib oling."""

GUIDE_FIRMA = """🏢 <b>Firma bo'limi (Hamkor)</b>

Biznes sheriklar va firmalar bilan qarzlarni <b>alohida boshqarish</b> uchun.

━━━━━━━━━━━━━━━━━━━━━━
➕ <b>Yangi firma qo'shish:</b>
1. Pastki menyudan <b>Hamkor</b> bo'limini oching
2. <b>Yangi firma</b> tugmasini bosing
3. To'ldiring:
   • Firma nomi ✦
   • Olib keluvchi ismi ✦
   • Telefon raqami ✦
   • Mahsulot soni ✦
   • Berilgan summa ✦
   • Qarz miqdori ✦
   • Izoh / sharhlar

━━━━━━━━━━━━━━━━━━━━━━
👁 Ko'rish · ✏️ O'zgartirish · 🗑 O'chirish

<i>(✦ — majburiy maydonlar)</i>"""

GUIDE_STATS = """📊 <b>Statistika va Hisobotlar</b>

━━━━━━━━━━━━━━━━━━━━━━
📈 <b>Statistika paneli</b> (Qarzdorlar sahifasi yuqorida):

🔢 <b>Jami qarzlar</b> — umumiy son
💵 <b>Jami summa</b> — umumiy miqdor
✅ <b>To'langan</b> — to'liq to'langan summa
⚠️ <b>Qarz qoldiq</b> — muddati o'tgan

━━━━━━━━━━━━━━━━━━━━━━
📄 <b>DOCX Shartnoma (Premium)</b>
Qarz → Ko'rish → <b>"DOCX yuklab olish"</b>

━━━━━━━━━━━━━━━━━━━━━━
🔍 <b>Filterlar:</b>
Hammasi · Aktiv · To'langan · Muddati o'tgan"""

GUIDE_NOTIF = """🔔 <b>Eslatmalar va Bildirishnomalar</b>

━━━━━━━━━━━━━━━━━━━━━━
⏰ <b>Avtomatik eslatmalar (Premium)</b>
Qarz qaytarish sanasidan oldin:
• <b>7 kun oldin</b> — ogohlantiruv
• <b>3 kun oldin</b> — eslatma
• <b>1 kun oldin</b> — yakuniy eslatma

━━━━━━━━━━━━━━━━━━━━━━
🔕 <b>Boshqarish</b>
Profil → Bildirishnomalar → O'chirish / Yoqish

━━━━━━━━━━━━━━━━━━━━━━
🔔 <b>Ko'rish</b>
Ilovaning yuqori o'ng burchagidagi 🔔 belgini bosing."""

GUIDE_SEC = f"""🔒 <b>Xavfsizlik va Maxfiylik</b>

━━━━━━━━━━━━━━━━━━━━━━
🛡 <b>Ma'lumotlar xavfsizligi</b>
• Barcha ma'lumotlar <b>shifrlangan</b>
• Faqat <b>siz</b> ko'ra olasiz
• Uchinchi shaxslarga <b>berilmaydi</b>
• Xavfsiz login tizimi bilan himoyalangan

━━━━━━━━━━━━━━━━━━━━━━
🔑 <b>Parolni o'zgartirish</b>
Profil → Xavfsizlik → "Parolni o'zgartirishni so'rash"
Telegram: {ADMIN_USERNAME}

━━━━━━━━━━━━━━━━━━━━━━
🗑 <b>Profilni o'chirish</b>
• 30 kun ichida tiklash mumkin
• Keyin butunlay o'chiriladi

━━━━━━━━━━━━━━━━━━━━━━
📱 Ko'p qurilmada ishlash mumkin — faqat login qiling."""

HELP_TEXT = """🆘 <b>Yordam Markazi</b>

❓ <b>Ko'p so'raladigan savollar</b> — tez javoblar
📞 <b>Admin bilan bog'lanish</b> — bevosita yordam

━━━━━━━━━━━━━━━━━━━━━━
⏰ Ish vaqti: <b>Har kuni 09:00–21:00</b>
✅ Dam olish kunlarida ham xizmat ko'rsatamiz"""

FAQ_TEXT = """❓ <b>Ko'p so'raladigan savollar</b>

Bo'lim tanlang 👇"""

FAQ_LOGIN = f"""🔐 <b>Kirish va Ro'yxatdan o'tish</b>

❓ <b>Qanday ro'yxatdan o'taman?</b>
Gmail yoki telefon raqam orqali. Ma'lumotlarni to'ldiring va parol yarating.

❓ <b>Parolimni unutdim?</b>
Profil → Xavfsizlik → "Parolni o'zgartirishni so'rash"
Telegram: {ADMIN_USERNAME}

❓ <b>Bir nechta qurilmada foydalanish?</b>
Ha, bir hisobdan turli qurilmalarda ishlash mumkin."""

FAQ_PAY = f"""💰 <b>Obuna va To'lovlar</b>

❓ <b>Obunasiz foydalanish?</b>
Ha, lekin 5 tagacha qarz. To'liq imkoniyatlar uchun obuna kerak.

❓ <b>Qaysi obuna tavsiya etiladi?</b>
⭐ <b>3 oylik</b> — eng mashhur, 15% chegirma bilan.

❓ <b>Qanday to'layman?</b>
Admin bilan bog'laning:
💬 {ADMIN_USERNAME} · 📞 {ADMIN_PHONE}

❓ <b>Obuna tugaganda?</b>
Avtomatik yangilanmaydi. Qo'lda uzaytirish kerak.

❓ <b>Bekor qilish?</b>
Yo'q, obuna bekor qilinmaydi."""

FAQ_DEBT_TEXT = """📝 <b>Qarz qo'shish va boshqarish</b>

❓ <b>Qarz qanday qo'shiladi?</b>
Qarzdorlar → "+" → Ma'lumot → Imzo → Saqlash.

❓ <b>Necha ta qarz?</b>
Bepul: <b>5 ta</b> · Premium: <b>cheksiz</b>

❓ <b>Tahrirlash mumkinmi?</b>
Ha → Ko'rish → Tahrirlash.

❓ <b>O'chirish mumkinmi?</b>
Ha, lekin <b>qaytarib bo'lmaydi!</b>

❓ <b>Imzo majburiy?</b>
Ha! Qonuniy tasdiqlash uchun majburiy.

❓ <b>Rasm yuklash?</b>
Ixtiyoriy. Dalil sifatida tavsiya etiladi."""

FAQ_STATS_TEXT = """📊 <b>Statistika va Hisobotlar</b>

❓ <b>Statistikani qayerda ko'raman?</b>
Qarzdorlar sahifasi → yuqori 4 ta karta:
Jami son · Jami summa · To'langan · Qoldiq

❓ <b>PDF / DOCX olish?</b>
Qarz → Ko'rish → <b>DOCX yuklab olish</b> (Premium)

❓ <b>Eslatma keladimi?</b>
Ha, Premium da <b>7, 3 va 1 kun oldin</b> avtomatik."""

FAQ_TECH = f"""📱 <b>Texnik savollar</b>

❓ <b>Qaysi qurilmalarda ishlaydi?</b>
✅ Android · ✅ iOS · ✅ Web brauzer

❓ <b>Dark mode?</b>
Ha → Profil → Tema → Qorang'u rejim.

❓ <b>Til o'zgartirish?</b>
Hozir faqat O'zbekcha. Rus/Ingliz tez orada.

❓ <b>Ko'p qarzni bir vaqtda qo'shish?</b>
Ha, Excel/CSV orqali import (Premium).

❓ <b>Muammo bo'lsa?</b>
💬 {ADMIN_USERNAME}
📞 {ADMIN_PHONE}
📧 {ADMIN_EMAIL}
⏰ Har kuni 09:00–21:00"""

CONTACT_TEXT = f"""📞 <b>Admin bilan bog'lanish</b>

👤 <b>Saidmaxmudov Rahmonsaid</b>

💬 Telegram: <b>{ADMIN_USERNAME}</b>
📞 Tel: <b>{ADMIN_PHONE}</b>
📧 Email: <b>{ADMIN_EMAIL}</b>

━━━━━━━━━━━━━━━━━━━━━━
⏰ Ish vaqti: <b>Har kuni 09:00–21:00</b>
✅ Dam olish kunlarida ham xizmat ko'rsatamiz"""


# ═════════════════════════════════════════════════════════════
#  COMMAND HANDLERS
# ═════════════════════════════════════════════════════════════

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    /start — ReplyKeyboard yuboradi.
    WebApp tugmasi klaviaturaning birinchi tugmasi (chap tep).
    """
    user = update.effective_user
    welcome = (
        f"Salom, <b>{user.first_name}</b>! 👋\n\n"
        "🏦 <b>MUOMILA</b> botiga xush kelibsiz!\n\n"
        "Pastdagi klaviaturadan bo'lim tanlang 👇\n\n"
        "🌐 <b>Ilova</b> — Telegramda Mini App ochadi\n"
        "ℹ️ <b>Biz haqimizda</b> — Ilova haqida ma'lumot\n"
        "💳 <b>Obuna</b> — Narxlar va sotib olish\n"
        "📖 <b>Qo'llanma</b> — Ilovani ishlatish\n"
        "🆘 <b>Yordam</b> — FAQ va admin"
    )
    await update.message.reply_text(
        welcome,
        reply_markup=main_reply_kb(),
        parse_mode="HTML",
    )


# ═════════════════════════════════════════════════════════════
#  MESSAGE HANDLER  (ReplyKeyboard tugmalarini ushlaydi)
# ═════════════════════════════════════════════════════════════

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "Biz haqimizda" in text:
        await update.message.reply_text(
            ABOUT_TEXT,
            parse_mode="HTML",
        )

    elif "Obuna" in text:
        await update.message.reply_text(
            SUBSCRIPTION_TEXT,
            reply_markup=sub_inline_kb(),
            parse_mode="HTML",
        )

    elif "Qo'llanma" in text or "Qollanma" in text:
        await update.message.reply_text(
            GUIDE_TEXT,
            reply_markup=guide_inline_kb(),
            parse_mode="HTML",
        )

    elif "Yordam" in text:
        await update.message.reply_text(
            HELP_TEXT,
            reply_markup=help_inline_kb(),
            parse_mode="HTML",
        )

    else:
        # Noma'lum xabar — klaviaturani qayta ko'rsatish
        await update.message.reply_text(
            "👇 Pastdagi tugmalardan birini tanlang:",
            reply_markup=main_reply_kb(),
            parse_mode="HTML",
        )


# ═════════════════════════════════════════════════════════════
#  CALLBACK HANDLER  (InlineKeyboard tugmalarini ushlaydi)
# ═════════════════════════════════════════════════════════════

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    d = query.data

    # ── Qo'llanma bo'limlari ───────────────────────────────
    if d == "back_guide":
        await query.edit_message_text(
            GUIDE_TEXT,
            reply_markup=guide_inline_kb(),
            parse_mode="HTML",
        )

    elif d == "g_debt":
        await query.edit_message_text(
            GUIDE_DEBT,
            reply_markup=back_guide_kb(),
            parse_mode="HTML",
            disable_web_page_preview=True,
        )

    elif d == "g_firma":
        await query.edit_message_text(
            GUIDE_FIRMA,
            reply_markup=back_guide_kb(),
            parse_mode="HTML",
        )

    elif d == "g_stats":
        await query.edit_message_text(
            GUIDE_STATS,
            reply_markup=back_guide_kb(),
            parse_mode="HTML",
        )

    elif d == "g_notif":
        await query.edit_message_text(
            GUIDE_NOTIF,
            reply_markup=back_guide_kb(),
            parse_mode="HTML",
        )

    elif d == "g_sec":
        await query.edit_message_text(
            GUIDE_SEC,
            reply_markup=back_guide_kb(),
            parse_mode="HTML",
        )

    # ── Yordam bo'limlari ──────────────────────────────────
    elif d == "back_help":
        await query.edit_message_text(
            HELP_TEXT,
            reply_markup=help_inline_kb(),
            parse_mode="HTML",
        )

    elif d == "faq":
        await query.edit_message_text(
            FAQ_TEXT,
            reply_markup=faq_inline_kb(),
            parse_mode="HTML",
        )

    elif d == "fq_login":
        await query.edit_message_text(
            FAQ_LOGIN,
            reply_markup=back_faq_kb(),
            parse_mode="HTML",
        )

    elif d == "fq_pay":
        await query.edit_message_text(
            FAQ_PAY,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬  Adminga yozish", url="https://t.me/Padiwakh_1")],
                [InlineKeyboardButton("◀️  FAQ ga qaytish",  callback_data="faq")],
            ]),
            parse_mode="HTML",
        )

    elif d == "fq_debt":
        await query.edit_message_text(
            FAQ_DEBT_TEXT,
            reply_markup=back_faq_kb(),
            parse_mode="HTML",
        )

    elif d == "fq_stats":
        await query.edit_message_text(
            FAQ_STATS_TEXT,
            reply_markup=back_faq_kb(),
            parse_mode="HTML",
        )

    elif d == "fq_tech":
        await query.edit_message_text(
            FAQ_TECH,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("💬  Adminga yozish", url="https://t.me/Padiwakh_1")],
                [InlineKeyboardButton("◀️  FAQ ga qaytish",  callback_data="faq")],
            ]),
            parse_mode="HTML",
        )

    elif d == "contact":
        await query.edit_message_text(
            CONTACT_TEXT,
            reply_markup=contact_inline_kb(),
            parse_mode="HTML",
        )


# ═════════════════════════════════════════════════════════════
#  ISHGA TUSHIRISH
# ═════════════════════════════════════════════════════════════

def main():
    """
    ApplicationBuilder:
    - concurrent_updates=True  → bir vaqtda 1000+ foydalanuvchi
    - run_polling               → uzluksiz ishlaydi
    """
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .concurrent_updates(True)   # ← 1000+ foydalanuvchi bir vaqtda
        .build()
    )

    # Handlerlar
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler)
    )

    logger.info("✅ MUOMILA bot ishga tushdi | concurrent_updates=True")
    app.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,   # eski xabarlarni o'tkazib yuboradi
    )


if __name__ == "__main__":
    asyncio.run(main())
