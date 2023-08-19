import telebot
import sqlite3
import config

bot = telebot.TeleBot(config.TOKEN)

def forward_to_main(message):
    if message.from_user.id != config.main_id:
        db = sqlite3.connect('users.db', check_same_thread=False)
        sql = db.cursor()
        sql.execute("SELECT user_id FROM blocked WHERE user_id = ?", (message.from_user.id,))
        if sql.fetchone() is None:
            forwarded_message = bot.forward_message(config.main_id, message.chat.id, message.message_id)
            sql.execute("INSERT OR IGNORE INTO USERS VALUES(?,?,?,?)", (message.from_user.id, message.from_user.first_name, forwarded_message.message_id, message.text))
            db.commit()
            bot.send_message(message.chat.id, config.text_message)
        else:
            bot.send_message(message.chat.id, config.banned)
        sql.close()
        db.close()

def forward_response_to_users(message):
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute("SELECT user_id FROM USERS WHERE messageid = ?", (message.reply_to_message.message_id,))
    Lusers = sql.fetchall()
    for user_id in Lusers:
        if message.content_type == "photo":
            capt = message.caption
            bot.send_photo(user_id[0], message.photo[-1].file_id, caption=capt)
        elif message.content_type == "video":
            capt = message.caption
            bot.send_video(user_id[0], message.video.file_id, caption=capt)
        elif message.content_type == "sticker":
            bot.send_sticker(user_id[0], message.sticker.file_id)
        # Add more content types here

def handle_text(message):
    pass  # Implement your text handling logic here

def handle_other_content_types(message):
    pass  # Implement your logic for handling other content types here

@bot.message_handler(content_types=['text', 'photo', 'video', 'sticker', 'audio', 'voice', 'document', 'location', 'animation', 'contact'])
def handle_messages(message):
    if message.chat.id == config.main_id:
        if message.reply_to_message is None:
            forward_to_main(message)
        else:
            forward_response_to_users(message)
    else:
        handle_text(message)

bot.polling(none_stop=True)
