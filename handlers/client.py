import os
from aiogram import types
from main import bot, dp
from utils.states import FSM
import pytube


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет. Я помогу тебе получить аудио дорожку из видео на YouTube. '
                                                 'Просто отправь мне ссылку на видео.')
    await FSM.get_href.set()


@dp.message_handler(state=FSM.get_href)
async def get_href(message: types.Message):
    href = message.text
    try:
        video = pytube.YouTube(href)
        videotitle = video.title
        video.streams.filter(only_audio=True).order_by('abr').last().download(r'.\downloaded', filename='audio.mp3')
        await bot.send_audio(message.from_user.id, open(r'.\downloaded\audio.mp3', 'rb'), title=videotitle)
        os.remove(r'.\downloaded\audio.mp3')

    except:
        await bot.send_message(message.from_user.id, 'Произошла ошибка: возможно, невалидная ссылка. '
                                                     'Попробуйте повторить отправку')
