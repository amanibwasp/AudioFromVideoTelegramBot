import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from main import bot, dp
from utils.states import FSM
import pytube
from handlers.messages import *
import moviepy.editor


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, start_message)
    await FSM.get_href.set()


@dp.message_handler(commands=['cancel'], state=FSM.get_href)
async def cancel_get_href(message: types.Message, state: FSMContext):
    await state.reset_state()
    await bot.send_message(message.from_user.id, canceled_message)


@dp.message_handler(state=FSM.get_href)
async def get_href(message: types.Message):
    href = message.text
    try:
        video = pytube.YouTube(href)
        videotitle = video.title
        video.streams.filter(res='360p', file_extension='mp4').first().download(r'.\downloaded',
                                                                                filename=fr'video{message.from_user.id}.mp4')
        audio = moviepy.editor.VideoFileClip(f"downloaded\\video{message.from_user.id}.mp4").audio
        audio.write_audiofile(fr'.\downloaded\audio{message.from_user.id}.mp3')
        await bot.send_audio(message.from_user.id, open(fr'.\downloaded\audio{message.from_user.id}.mp3', 'rb'),
                             title=videotitle)
        os.remove(fr'.\downloaded\audio{message.from_user.id}.mp3')
        os.remove(fr'.\downloaded\video{message.from_user.id}.mp4')
        await bot.send_message(message.from_user.id, done_message)
    except Exception as ex:
        await bot.send_message(message.from_user.id, error_message)
        print(ex)
