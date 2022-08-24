import logging
from aiogram import Bot, Dispatcher, executor, types

from oxfordLookUp import getDefinitions
from googletrans import Translator
translator = Translator()

API_TOKEN = '5390074419:AAEbDYMQYt_dBQ7kk85ahCrwNsPSaxyhMiI'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

    await message.reply("Asalamu alaykum! Enlish speak ,translate botga hush kelibsiz. ")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):

    await message.reply("Asalamu alaykum! Sizga qanday yordam bera olaman ")


@dp.message_handler()
async def translator_send(message: types.Message):
   lang = translator.detect(message.text).lang
   if len(message.text.split())>2:
       dest = "uz" if lang == 'en' else 'en'
    # await bot.send_message(message.chat.id, message.text)
       await message.reply(translator.translate(message.text,dest).text)
   else:
       word_id = message.text

       if lang != 'en':
           word_id = translator.translate(message.text,dest='en').text
           if len(word_id) >= 2:
               await message.reply(word_id)

       lookup = getDefinitions(word_id)


       if lookup:
            await message.reply(f"Word: {word_id} \nDefinitions:\n{lookup['definitions']}")
            if lookup.get('audio'):
                await message.reply_voice(lookup['audio'])
            else:
                await message.reply("Bunday so'z topilmadi !")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)