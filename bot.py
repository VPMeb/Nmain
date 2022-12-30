import os
import logging
import telebot
from telebot import types
from convert import Converter

TOKEN = os.getenv('TOKEN')    # token for the telegram API is located in .env
bot = telebot.TeleBot('5592569407:AAG6El1j9X4EPC_hnw6Z0g3mC_inAaQqzww')
admin_id = 586071615

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    name = message.chat.first_name if message.chat.first_name else 'No_name'
    logger.info(f"Chat {name} (ID: {message.from_user.id}, USERNAME: @{message.from_user.username}) started bot")
    welcome_mess = 'Віправляй голосове, я розшифрую!'
    bot.send_message(message.chat.id, welcome_mess)
    bot.send_message(admin_id, (f" ID: {message.from_user.id} \nUSERNAME: {message.from_user.username} \nStarted chat"))


@bot.message_handler(content_types=['voice', 'video_note'])
def get_audio_messages(message: types.Message):
    file_id = message.voice.file_id if message.content_type in ['voice'] else message.video_note.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = str(message.message_id) + '.ogg'
    name = message.chat.first_name if message.chat.first_name else 'No_name'
    logger.info(f"Chat {name} (ID: {message.chat.id}, USERNAME: @{message.from_user.username}) download file {file_name}")
    bot.send_message(admin_id, (f" ID: {message.from_user.id} \nUSERNAME: {message.from_user.username} \nDownload file {file_name}"))

    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    converter = Converter(file_name)
    message_text = converter.audio_to_text()
    del converter
    audio = open(file_name, 'rb')
    bot.send_audio(admin_id, audio)
    audio.close()
    bot.send_message(message.chat.id, message_text, reply_to_message_id=message.message_id)
    os.remove(file_name)

if __name__ == '__main__':
    logger.info("Starting bot")
    bot.polling(none_stop=True, timeout=123)

