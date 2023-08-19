import telebot
import sqlite3
import config

bot = telebot.TeleBot(config.TOKEN)

def create_db_new():
    db = sqlite3.connect('users.db', check_same_thread=False)
    sql = db.cursor()
    sql.execute('''CREATE TABLE IF NOT EXISTS USERS(
        user_id INTEGER,
        first_name VARCHAR,
        messageid INT,
        message VARCHAR)''')
    sql.execute('''CREATE TABLE IF NOT EXISTS blocked(
        user_id INT)''')
    sql.execute('''CREATE TABLE IF NOT EXISTS user(
        user_id INT)''')
    sql.close()
    db.close()

create_db_new()

@bot.message_handler(commands=['start'])
def handle_start(message):
    start(message)

@bot.message_handler(commands=["ban"])
def handle_ban(message):
    blocked(message)

@bot.message_handler(commands=["unban"])
def handle_unban(message):
    unblocked(message)

@bot.message_handler(commands=["admin_message"])
def handle_admin_message(message):
    if message.chat.id == config.main_id:
        bot.send_message(message.chat.id, "Enter the message you want to send:")
        bot.register_next_step_handler(message, handle_admin_message_next)
    else:
        pass

def handle_admin_message_next(message):
    message_everyone(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    text(message)

@bot.message_handler(content_types=['photo','sticker','video','audio','voice','location','animation','contact','document','dice','poll'])
def handle_other(message):
    other(message)

try:
    bot.polling(none_stop=True)
except Exception as e:
    print("An error occurred:", e)
