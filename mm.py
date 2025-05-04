from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, CallbackQueryHandler
import logging

TOKEN = "7884677695:AAE_5hhFYGD7qFZPC9I70dBFxV5qa66Vrpg"

# Referal maglumatlary
users = {}

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def main_menu():
    keyboard = [
        [InlineKeyboardButton("📨 Получить реф. ссылку", callback_data='ref')],
        [InlineKeyboardButton("📊 Статистика", callback_data='stats')],
        [InlineKeyboardButton("📅 О конкурсе", callback_data='about')],
        [InlineKeyboardButton("ℹ️ О боте", callback_data='bot')]
    ]
    return InlineKeyboardMarkup(keyboard)

def start(update: Update, context: CallbackContext):
    user = update.effective_user
    user_id = str(user.id)
    args = context.args

    if user_id not in users:
        users[user_id] = {"referrals": 0, "username": user.username}

        if args:
            ref_id = args[0]
            if ref_id != user_id and ref_id in users:
                users[ref_id]["referrals"] += 1

                # Referal linkiň eýesine habar gitmeli
                context.bot.send_message(
                    chat_id=int(ref_id),
                    text=f"🎉 У вас новый реферал: @{user.username or user.first_name}!"
                )

    update.message.reply_text("👋 Привет! Добро пожаловать в конкурс бота!", reply_markup=main_menu())

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    user_id = str(query.from_user.id)

    if query.data == "ref":
        link = f"https://t.me/konursbot?start={user_id}"
        keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data='main')]]
        query.edit_message_text(f"🔗 Ваша реферальная ссылка:\n{link}", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "stats":
        text = "🏆 Топ 10 участников по рефералам:\n"
        top_users = sorted(users.items(), key=lambda x: x[1]["referrals"], reverse=True)[:10]
        for i, (uid, data) in enumerate(top_users, start=1):
            username = data['username'] or f"user_{uid}"
            text += f"{i}. @{username} - {data['referrals']} рефералов\n"
        user_ref = users.get(user_id, {}).get("referrals", 0)
        rank = [i for i, (uid, _) in enumerate(top_users, start=1) if uid == user_id]
        if rank:
            text += f"\n📌 Ваша позиция: {rank[0]} ({user_ref} рефералов)"
        else:
            text += f"\n📌 Вы еще не в топе. У вас {user_ref} рефералов."
        keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data='main')]]
        query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "bot":
        text = (
            "🤖 О боте:\n\n"
            "💬 Группа: https://t.me/+BW73WJdKFK1jMmZi\n"
            "📢 Канал: https://t.me/onlinekonkrs\n"
            "👤 Администратор: https://t.me/CCCR_RUSS"
        )
        keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data='main')]]
        query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "about":
        text = (
            "📅 Конкурс проводится до: **15.05.2025**\n"
            "🏆 Награды:\n"
            "🥇 1 место — ⭐ 1000 Telegram Stars\n"
            "🥈 2 место — ⭐ 500 Telegram Stars\n"
            "🥉 3 место — ⭐ 300 Telegram Stars"
        )
        keyboard = [[InlineKeyboardButton("🔙 Главное меню", callback_data='main')]]
        query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "main":
        query.edit_message_text("🔙 Главное меню:", reply_markup=main_menu())

def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("❓ Я не понимаю эту команду. Используйте /start.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
