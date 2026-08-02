import logging
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

COMPOUND_CAPITAL, COMPOUND_RISK, COMPOUND_ENTRY, COMPOUND_SL, COMPOUND_TP = range(5)

MAIN_KEYBOARD = [
    ['🚀 ابدأ (Start)', 'ℹ️ عن WOLF'],
    ['قناة التوصيات 📈', '📚 المحاضرات'],
    ['🎯 حاسبة الصفقات المركبة', '📅 أجندة الأخبار'],
    ['🧠 اختبار المعرفة', '🚨 تنبيهات الذهب'],
    ['قناة الأخبار 🚨', '🕰️ أوقات الجلسات'],
    ['🎫 الدعم الفني', 'ℹ️ عن WOLF']
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(f"أهلاً بك يا {user_name} في بوت WOLF IQ 🐺\n\nاضغط على زر **🚀 ابدأ (Start)** أو اختر من القائمة أدناه:", reply_markup=reply_markup)
    return ConversationHandler.END

async def compound_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎯 **حاسبة الصفقات المركبة**\n\nالرجاء إدخال حجم رأس المال بالدولار ($):")
    return COMPOUND_CAPITAL

async def compound_capital(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['capital'] = float(update.message.text.replace('$', '').strip())
        await update.message.reply_text("أدخل نسبة المخاطرة (٪):")
        return COMPOUND_RISK
    except ValueError:
        await update.message.reply_text("⚠️ يرجى إدخال رقم صحيح:")
        return COMPOUND_CAPITAL

async def compound_risk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['risk'] = float(update.message.text.replace('%', '').strip())
        await update.message.reply_text("أدخل سعر الدخول:")
        return COMPOUND_ENTRY
    except ValueError:
        await update.message.reply_text("⚠️ يرجى إدخال رقم صحيح:")
        return COMPOUND_RISK

async def compound_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['entry'] = float(update.message.text.strip())
        await update.message.reply_text("أدخل سعر وقف الخسارة (SL):")
        return COMPOUND_SL
    except ValueError:
        await update.message.reply_text("⚠️ يرجى إدخال سعر دخول صحيح:")
        return COMPOUND_ENTRY

async def compound_sl(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['sl'] = float(update.message.text.strip())
        await update.message.reply_text("أدخل سعر الهدف (TP):")
        return COMPOUND_TP
    except ValueError:
        await update.message.reply_text("⚠️ يرجى إدخال وقف خسارة صحيح:")
        return COMPOUND_SL

async def compound_tp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        tp = float(update.message.text.strip())
        cap = context.user_data['capital']
        risk_p = context.user_data['risk']
        entry = context.user_data['entry']
        sl = context.user_data['sl']
        
        sl_pips = abs(entry - sl) * 10
        tp_pips = abs(tp - entry) * 10
        risk_amt = cap * (risk_p / 100.0)
        lot = risk_amt / (sl_pips * 10.0) if sl_pips > 0 else 0.01
        
        reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
        await update.message.reply_text(
            f"🎯 **نتيجة الحاسبة المركبة:**\n\n"
            f"👉 حجم العقد المناسب: `{lot:.2f} Lot`\n"
            f"🔴 الخسارة المحتملة: ${risk_amt:,.2f}\n"
            f"🟢 الربح المحتمل: ${tp_pips * 10.0 * lot:,.2f}",
            parse_mode="Markdown", reply_markup=reply_markup
        )
        return ConversationHandler.END
    except ValueError:
        await update.message.reply_text("⚠️ يرجى إدخال سعر هدف صحيح:")
        return COMPOUND_TP

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text("تم الإلغاء.", reply_markup=reply_markup)
    return ConversationHandler.END

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    
    if 'ابدأ' in text:
        user_name = update.effective_user.first_name
        reply_markup = ReplyKeyboardMarkup(MAIN_KEYBOARD, resize_keyboard=True)
        await update.message.reply_text(f"مرحباً بك مجدداً يا {user_name}! 🐺\n\nأنت جاهز تماماً الآن، اختر ما يناسبك من الأزرار أدناه:", reply_markup=reply_markup)
        
    elif 'التوصيات' in text:
        kb = [[InlineKeyboardButton("🔗 الانضمام لقناة التوصيات", url="https://t.me/+c7_BCwvYh6UwYzRi")]]
        await update.message.reply_text("📈 **قناة التوصيات:**", reply_markup=InlineKeyboardMarkup(kb))
        
    elif 'المحاضرات' in text:
        kb = [[InlineKeyboardButton("🔗 الانضمام لقناة المحاضرات", url="https://t.me/+buOAkwf4Np9lYzAy")]]
        await update.message.reply_text("📚 **قناة المحاضرات:**", reply_markup=InlineKeyboardMarkup(kb))
        
    elif 'أجندة' in text:
        await update.message.reply_text("📅 **أجندة الأخبار الاقتصادية:**\n- مؤشر التضخم CPI\n- قرار الفائدة الفيدرالي")
        
    elif 'الأخبار' in text:
        kb = [[InlineKeyboardButton("🔗 الانضمام لقناة الأخبار", url="https://t.me/+Er34wPWoVHY3MjMy")]]
        await update.message.reply_text("🚨 **قناة الأخبار:**", reply_markup=InlineKeyboardMarkup(kb))
        
    elif 'الجلسات' in text:
        await update.message.reply_text(
            "🕰️ **أوقات الجلسات الرئيسية (توقيت مكة المكرمة):**\n\n"
            "🇦🇺 **جلسة سيدني:** 01:00 ص - 10:00 ص\n"
            "🇯🇵 **جلسة طوكيو:** 03:00 ص - 12:00 م\n"
            "🇬🇧 **جلسة لندن:** 10:00 ص - 07:00 م\n"
            "🇺🇸 **جلسة نيويورك:** 03:00 م - 12:00 ص\n\n"
            "🔥 **أقوى السيولة والحركة تكون في تقاطع لندن مع نيويورك (من 03:00 م إلى 07:00 م).**"
        )
        
    elif 'تنبيهات الذهب' in text:
        kb = [[InlineKeyboardButton("🔔 قناة تنبيهات الذهب", url="https://t.me/+c7_BCwvYh6UwYzRi")]]
        await update.message.reply_text(
            "🚨 **نظام تنبيهات الذهب (XAUUSD):**\n\n"
            "يتم إرسال تنبيهات فورية عند وصول السعر لمناطق العرض والطلب الرئيسية أو كسر المستويات الهامة.\n"
            "اضغط بالأسفل للانضمام لقناة التنبيهات المخصصة:", 
            reply_markup=InlineKeyboardMarkup(kb)
        )
        
    elif 'اختبار المعرفة' in text:
        kb = [
            [InlineKeyboardButton("✅ صح", callback_data="tf_q1_wrong"), InlineKeyboardButton("❌ خطأ", callback_data="tf_q1_right")]
        ]
        await update.message.reply_text(
            "🧠 **اختبار المعرفة (صح أو خطأ - 5 أسئلة):**\n\n"
            "**السؤال 1 من 5:**\n"
            "المخاطرة بأكثر من 50% من رأس المال في صفقة واحدة تعتبر إدارة رأس مال سليمة.",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        
    elif 'الدعم' in text:
        kb = [[InlineKeyboardButton("💬 الدعم الفني", url="https://t.me/wolf_iq_support")]]
        await update.message.reply_text("🎫 للتواصل مع الدعم الفني:", reply_markup=InlineKeyboardMarkup(kb))
        
    elif 'عن WOLF' in text:
        await update.message.reply_text(
            "ℹ️ **عن WOLF:**\n\n"
            "WOLF منصة متخصصة في تداول الذهب، بخبرة تمتد لأكثر من 5 سنوات في الأسواق المالية. "
            "ساعدنا أكثر من 8,000 متداول على تطوير مهاراتهم، ووصلت خدماتنا إلى أكثر من 13 دولة. "
            "نوفر توصيات احترافية، نظامًا تعليميًا متكاملًا، وإدارة فعّالة لرأس المال، لنمنح المتداولين تجربة مبنية على المعرفة والانضباط. 🐺"
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Q1 Handler
    if data == "tf_q1_right":
        kb = [[InlineKeyboardButton("✅ صح", callback_data="tf_q2_right"), InlineKeyboardButton("❌ خطأ", callback_data="tf_q2_wrong")]]
        await query.edit_message_text("✅ **إجابة صحيحة!**\n\n**السؤال 2 من 5:**\nالرمز العالمي لتداول الذهب في الأسواق المالية هو XAUUSD.", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "tf_q1_wrong":
        kb = [[InlineKeyboardButton("🔄 إعادة الاختبار", callback_data="tf_q1_right")]]
        await query.edit_message_text("❌ **إجابة خاطئة!** المخاطرة بأكثر من نصف الحساب تدمر المحفظة فوراً.", reply_markup=InlineKeyboardMarkup(kb))

    # Q2 Handler
    elif data == "tf_q2_right":
        kb = [[InlineKeyboardButton("✅ صح", callback_data="tf_q3_wrong"), InlineKeyboardButton("❌ خطأ", callback_data="tf_q3_right")]]
        await query.edit_message_text("✅ **إجابة صحيحة!**\n\n**السؤال 3 من 5:**\nأمر وقف الخسارة (Stop Loss) ليس له أي أهمية ويمكن الاستغناء عنه تماماً في الصفقات.", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "tf_q2_wrong":
        kb = [[InlineKeyboardButton("🔄 إعادة الاختبار", callback_data="tf_q1_right")]]
        await query.edit_message_text("❌ **إجابة خاطئة!** الذهب يرمز له بـ XAUUSD.", reply_markup=InlineKeyboardMarkup(kb))

    # Q3 Handler
    elif data == "tf_q3_right":
        kb = [[InlineKeyboardButton("✅ صح", callback_data="tf_q4_right"), InlineKeyboardButton("❌ خطأ", callback_data="tf_q4_wrong")]]
        await query.edit_message_text("✅ **إجابة صحيحة!**\n\n**السؤال 4 من 5:**\nتقاطع جلسة لندن مع جلسة نيويورك يشهد أعلى سيولة وحركة في السوق.", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "tf_q3_wrong":
        kb = [[InlineKeyboardButton("🔄 إعادة الاختبار", callback_data="tf_q1_right")]]
        await query.edit_message_text("❌ **إجابة خاطئة!** وقف الخسارة أساسي لحماية الحساب.", reply_markup=InlineKeyboardMarkup(kb))

    # Q4 Handler
    elif data == "tf_q4_right":
        kb = [[InlineKeyboardButton("✅ صح", callback_data="tf_q5_wrong"), InlineKeyboardButton("❌ خطأ", callback_data="tf_q5_right")]]
        await query.edit_message_text("✅ **إجابة صحيحة!**\n\n**السؤال 5 والأخير:**\nالاعتماد على الحظ والتوقعات العشوائية هو الطريق الأساسي للنجاح المستدام في التداول.", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "tf_q4_wrong":
        kb = [[InlineKeyboardButton("🔄 إعادة الاختبار", callback_data="tf_q1_right")]]
        await query.edit_message_text("❌ **إجابة خاطئة!** تقاطع لندن ونيويورك هو الأقوى سيولة.", reply_markup=InlineKeyboardMarkup(kb))

    # Q5 Handler (Final)
    elif data == "tf_q5_right":
        kb = [[InlineKeyboardButton("🔄 إعادة الاختبار", callback_data="tf_q1_right")]]
        await query.edit_message_text("🎉 **ألف مبروك! اجتزت اختبار الـ 5 أسئلة بنجاح تام!** 🐺\n\nأنت تملك أساسيات واعية للانضباط وإدارة المخاطر.", reply_markup=InlineKeyboardMarkup(kb))
    elif data == "tf_q5_wrong":
        kb = [[InlineKeyboardButton("🔄 إعادة الاختبار", callback_data="tf_q1_right")]]
        await query.edit_message_text("❌ **إجابة خاطئة!** التداول يعتمد على العلم والانضباط وليس الحظ.", reply_markup=InlineKeyboardMarkup(kb))

if __name__ == '__main__':
    TOKEN = '8875523694:AAGh7572AbsfyaGN-C-F1624vkpy0UYN-cc'
    app = ApplicationBuilder().token(TOKEN).build()

    compound_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('حاسبة الصفقات المركبة'), compound_start)],
        states={
            COMPOUND_CAPITAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, compound_capital)],
            COMPOUND_RISK: [MessageHandler(filters.TEXT & ~filters.COMMAND, compound_risk)],
            COMPOUND_ENTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, compound_entry)],
            COMPOUND_SL: [MessageHandler(filters.TEXT & ~filters.COMMAND, compound_sl)],
            COMPOUND_TP: [MessageHandler(filters.TEXT & ~filters.COMMAND, compound_tp)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(compound_handler)
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("Bot is running now...")
    app.run_polling()