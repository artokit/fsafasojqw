from pyrogram import Client
from pyrogram import types, filters
from aiogram import Bot
import os
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Ключ - откуда копируем, значение - куда копируем.
CHANNELS = {
    -1001544589722: [-1002048622883],
    -1001950740884: [-1001858537505]
}
api_id = 11325071
api_hash = '8b7bd8121748973fcc1341afb5935b3b'
app = Client('anon', api_id=api_id, api_hash=api_hash)
TOKEN = '6487800433:AAHGvtLYd-TYjqw7KpcVOV6NElEdzlkawpE'
bot = Bot(token=TOKEN)
DOWNLOADS = {}

keyboard = InlineKeyboardMarkup()
keyboard.row(
    InlineKeyboardButton('🚀Регистрация🚀', url='https://cashmoney.beauty/7ynxnfsL?sub2=SNG')
)
keyboard.row(
    InlineKeyboardButton('Моя личка📧', url='https://t.me/danyaa_lucky')
)


async def edit_keyboard(msg):
    await bot.edit_message_reply_markup(msg.chat.id, msg.id, reply_markup=keyboard)


def replace_sender(txt):
    if txt:
        return txt.replace(
            '@DanyaLucky_bot', '@danyaa_lucky'
        ).replace(
            'https://t.me/DanyaLucky_bot', 'https://t.me/danyaa_lucky'
        ).replace(
            '@Luck_Dany', '@danyaa_lucky'
        ).replace(
            '1wdkmb.top', 'https://cashmoney.beauty/7ynxnfsL?sub2=SNG'
        )
    return txt


@app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.text)
async def post_text_handler(client: Client, message: types.Message):
    await send_in_groups(client.send_message, message.chat.id, text=replace_sender(message.text))


@app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.media_group)
async def post_media_handler(client: Client, message: types.Message):
    length = len((await message.get_media_group()))
    res = await client.download_media(message)
    prev_res = DOWNLOADS.get(message.media_group_id, {}).get('res', [])
    prev_res.append([res, message.caption])
    DOWNLOADS[message.media_group_id] = {'length': length, 'res': prev_res}

    if DOWNLOADS[message.media_group_id]['length'] == len(prev_res):
        groups = []
        for i in DOWNLOADS[message.media_group_id]['res']:
            frmt = i[0][::-1].split('.')[0][::-1].lower()

            if frmt in ('jpg', 'png'):
                groups.append(types.InputMediaPhoto(i[0], caption=replace_sender(i[1])))

            if frmt in ('mp4', 'avi'):
                groups.append(types.InputMediaVideo(i[0], caption=replace_sender(i[1])))

        await send_in_groups(client.send_media_group, message.chat.id, kb=False, media=groups)

        for i in DOWNLOADS[message.media_group_id]['res']:
            os.remove(i[0])

        del DOWNLOADS[message.media_group_id]


@app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.photo)
async def post_photo_handler(client: Client, message: types.Message):
    res = await client.download_media(message)
    await send_in_groups(client.send_photo, message.chat.id, photo=res, caption=replace_sender(message.caption))

    os.remove(res)


@app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.video)
async def post_video_handler(client: Client, message: types.Message):
    res = await client.download_media(message)
    await send_in_groups(client.send_video, message.chat.id, video=res, caption=replace_sender(message.caption))

    os.remove(res)


@app.on_message(filters=filters.chat(list(CHANNELS.keys())) & filters.video_note)
async def post_video_note_handler(client: Client, message: types.Message):
    res = await client.download_media(message)
    await send_in_groups(client.send_video_note, message.chat.id, kb=False, video_note=res)

    os.remove(res)


async def send_in_groups(func, chat_copy_id, kb=True, **kwargs):
    for i in CHANNELS[chat_copy_id]:
        try:
            msg = await func(
                i,
                **kwargs
            )
            if kb:
                await edit_keyboard(msg)
        except Exception as e:
            print(f'Исключение в канале {i}\n{str(e)}')


app.run()
