from pyrogram import filters
from pyrogram.types import Message

def register(bot, handler_list):
    h = bot.on_message(filters.command("start") & filters.private)(start_handler)
    handler_list.append(h)

async def start_handler(client, message: Message):
    await message.reply_text(
        "Halo! Bot siap digunakan.\n\n"
        "tes tes tes\n"
        "BALERAROBY\n\n"
        "Halo"
    )
