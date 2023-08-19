import telebot
import sqlite3
import config

bot = telebot.TeleBot(config.TOKEN)

def handle_text_message(message):
    try:
        db = sqlite3.connect('users.db', check_same_thread=False)
        sql = db.cursor()
        
        # Check if user is blocked
        sql.execute("SELECT user_id FROM blocked WHERE user_id = ?", (message.from_user.id,))
        if sql.fetchone() is not None:
            bot.send_message(message.chat.id, config.banned)
        else:
            if message.chat.id != config.main_id:
                # Forward message to main chat
                forwarded_message = bot.forward_message(config.main_id, message.chat.id, message.message_id)
                sql.execute("INSERT OR IGNORE INTO USERS VALUES(?,?,?,?)", (message.from_user.id, message.from_user.first_name, forwarded_message.message_id, message.text))
                db.commit()
                bot.send_message(message.chat.id, config.text_message)
                print(message.message_id)
            elif message.chat.id == config.main_id:
                if message.reply_to_message is None:
                    # Forward message within main chat
                    forwarded_message = bot.forward_message(config.main_id, message.chat.id, message.message_id)
                    sql.execute("INSERT INTO USERS VALUES(?,?,?,?)", (message.from_user.id, message.from_user.first_name, forwarded_message.message_id, message.text))
                    db.commit()
                    bot.send_message(message.chat.id, config.text_message)
                elif message.reply_to_message is not None:
                    print(message.reply_to_message.message_id)
                    sql.execute("SELECT user_id FROM USERS WHERE messageid = ?", (message.reply_to_message.message_id,))
                    db.commit()
                    recipient_user_ids = sql.fetchall()
                    for user_id in recipient_user_ids:
                        print(user_id[0])
                        bot.send_message(user_id[0], message.text)
        
        sql.close()
        db.close()
    except Exception as e:
        print("Error:", str(e))
        bot.send_message(message.chat.id, config.blocked)

@bot.message_handler(content_types=['text'])
def handle_messages(message):
    handle_text_message(message)

bot.polling(none_stop=True)
