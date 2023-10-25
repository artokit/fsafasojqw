from aiogram import Bot, Dispatcher, executor
from aiogram.types import ChatJoinRequest, ChatMemberUpdated

token = '6382545014:AAEtwUyxvyn5WbYU0ZX_lWNlYANV3854hqE'
bot = Bot(token)
dp = Dispatcher(bot)
TEXT_APPROVE_USER = 'Братан, Привет. Рад тебя видеть в нашем канале!'
TEXT_LEAVE_USER = 'Ты нахуя это сделал?'
CHANNEL_ID = -1002002645618


@dp.chat_join_request_handler(chat_id=CHANNEL_ID)
async def approve_user(update: ChatJoinRequest):
    await update.approve()
    await bot.send_message(chat_id=update.from_user.id, text=TEXT_APPROVE_USER)


@dp.chat_member_handler(chat_id=CHANNEL_ID)
async def leave_user(chat_member_updated: ChatMemberUpdated):
    if chat_member_updated.new_chat_member.status == 'left':
        await bot.send_message(
            chat_member_updated.from_user.id,
            TEXT_LEAVE_USER
        )


executor.Executor(dp).start_polling(allowed_updates=["message", "inline_query", "chat_member", 'chat_join_request'])
