from Zaid import app
from pyrogram import filters


@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
   await message.reply_text("●[ Bʌcʜʜo ĸo pʜŋ📱 ʌʋr cʜʋtɩƴO 💦ĸo ɗɩɭ ɗoʛɘ♥ to wo ʛʌɱɘ ʜɩ ĸʜɘɭɘŋʛɘ ]🥴🤣")
