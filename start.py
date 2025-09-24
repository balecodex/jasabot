# start.py
from pyrogram import filters
from pyrogram.types import Message

def register(bot):
    @bot.on_message(filters.command("start") & filters.private)
    async def start_handler(client, message: Message):
        await message.reply_text(
            "Halo! Bot siap digunakan.\n\n"
            "tes tes tes"
            "BALERAROBY"
        )
