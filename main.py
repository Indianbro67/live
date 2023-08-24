import telebot
import sqlite3
from plugins.ban import blocked
import time
from plugins.unban import unblocked
from content.text import text
from content.other import other
from plugins.start import start
from plugins.everyone_message import message_everyone

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

import config
bot = telebot.TeleBot(config.TOKEN)

# Sticker ID to be sent when the user starts the bot
start_sticker_id = "CAACAgUAAxkBAAEJ3rdkx-mv7czAKR0AAR_OcrzAvG838cAAAucLAAIUT0FWDj56XbQhG4UvBA"

@bot.message_handler(commands=['start'])
def start2(message):
    # Send the sticker
    bot.send_sticker(message.chat.id, start_sticker_id)

    # Send image by URL and use the start variable in the caption
    image_url = "https://justpaste.it/img/small/279b70b0a58f94a0228979a8087f7ea7.jpg"  # Replace with the actual image URL
    caption = (
        "𝐖𝐞 𝐒𝐭𝐫𝐢𝐜𝐭𝐥𝐲,\n"
        "        𝗱𝗼𝗻'𝘁 𝗮𝗹𝗹𝗼𝘄 𝘁𝗼 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘀𝘁𝘂𝗱𝘆 𝗺𝗮𝘁𝗲𝗿𝗶𝗮𝗹 𝗮𝗻𝗱 𝗺𝗼𝘃𝗶𝗲𝘀 . "
        "𝗜𝗳 𝘆𝗼𝘂 𝗱𝗼𝘄𝗻𝗹𝗼𝗮𝗱 𝘄𝗶𝘁𝗵𝗼𝘂𝘁 𝗯𝗼𝘁 𝗼𝘄𝗻𝗲𝗿 𝗽𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻 𝘆𝗼𝘂 𝘄𝗶𝗹𝗹 𝗱𝗶𝗿𝗲𝗰𝘁𝗹𝘆 𝗯𝗮𝗻 𝗳𝗿𝗼𝗺 𝗯𝗼𝘁"
        + (message.text.split(' ', 1)[1] if len(message.text.split(' ', 1)) > 1 else '')
    )
    bot.send_photo(message.chat.id, image_url, caption=caption)

@bot.message_handler(commands=["ban"])
def bloc(message):
    blocked(message)

@bot.message_handler(commands=["unban"])
def some(message):
    unblocked(message)

@bot.message_handler(commands=["admin_message"])
def reklama(message):
    if message.chat.id == config.main_id:
        bot.send_message(message.chat.id, "your message to be sent: ")
        bot.register_next_step_handler(message, textrek)
    else:
        pass

def textrek(message):
    message_everyone(message)

@bot.message_handler(content_types=['text'])
def tex(message):
    text(message)

# photo, sticker, video
@bot.message_handler(content_types=['photo', 'sticker', 'video', 'audio', 'voice', 'location', 'animation', 'contact', 'document', 'dice', 'poll'])
def other2(message):
    other(message)

bot.polling(none_stop=True)
