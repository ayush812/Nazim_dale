import pyrogram
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup,InlineKeyboardButton
import bypasser
import os
import ddl
import requests
import threading
from texts import HELP_TEXT
from bypasser import ddllist


# bot
bot_token = os.environ.get("TOKEN", "5744177498:AAGLqXNrjKtSmR9o6CrvhD1tkwJMBvmAO44")
api_hash = os.environ.get("HASH", "fbe8a002efe8427759371eab5809f1de") 
api_id = os.environ.get("ID", "18123144")
app = Client("my_bot",api_id=api_id, api_hash=api_hash,bot_token=bot_token)  


# loop thread
def loopthread(message):
    urls = []
    for ele in message.text.split():
        if "http://" in ele or "https://" in ele:
            urls.append(ele)
    if len(urls) == 0:
        return

    if bypasser.ispresent(ddllist,urls[0]):
        msg = app.send_message(message.chat.id, "⚡ __generating...__", reply_to_message_id=message.id)
    else:
        if urls[0] in "https://olamovies" or urls[0] in "https://psa.pm/":
            msg = app.send_message(message.chat.id, "🔎 __this might take some time...__", reply_to_message_id=message.id)
        else:
            msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)

    link = ""
    for ele in urls:
        if bypasser.ispresent(ddllist,ele):
            try: temp = ddl.direct_link_generator(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        else:    
            try: temp = bypasser.shortners(ele)
            except Exception as e: temp = "**Error**: " + str(e)
        print("bypassed:",temp)
        link = link + temp + "\n\n"
        
    try: app.edit_message_text(message.chat.id, msg.id, f'__{link}__', disable_web_page_preview=True)
    except: app.edit_message_text(message.chat.id, msg.id, "__Failed to Bypass__")


# start command
@app.on_message(filters.command(["start"]))
def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, f"__👋 ʜɪ **{message.from_user.mention}**, ɪ ᴀᴍ ᴀᴅᴠᴀɴᴄᴇ ʟɪɴᴋ ʙʏᴘᴀssᴇʀ ʙᴏᴛ, ᴊᴜsᴛ sᴇɴᴅ ᴍᴇ ᴀɴʏ sᴜᴘᴘᴏʀᴛᴇᴅ ʟɪɴᴋs ᴀɴᴅ ɪ ᴡɪʟʟ ʏᴏᴜ ɢᴇᴛ ʏᴏᴜ ʀᴇsᴜʟᴛs.\nCheckout /help ᴛᴏ ʀᴇᴀᴅ ᴍᴏʀᴇ__",
    reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("💌 𝙼𝙾𝚅𝙸𝙴 𝙱𝙾𝚃 💌", url="https://t.me/mkvCinemastg_Bot")],[InlineKeyboardButton("⚡ 𝚄𝙿𝙳𝙰𝚃𝙴𝚂 ⚡", url="https://t.me/skmovieslinks")],
                                     [InlineKeyboardButton("📺 24/7 𝙼𝙾𝚅𝙸𝙴𝚂 📺", url="https://t.me/skymovieshdlinks"), InlineKeyboardButton("💎TV SHOWS💎", url="https://t.me/Serials_Before_Tv")],
                                     [ InlineKeyboardButton("🌐 Source Code", url="https://te.legra.ph/file/2184b7d4cd6fa1cfc8ac4.mp4")]]), reply_to_message_id=message.id)


# help command
@app.on_message(filters.command(["help"]))
def send_help(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    app.send_message(message.chat.id, HELP_TEXT, reply_to_message_id=message.id, disable_web_page_preview=True)


# links
@app.on_message(filters.text)
def receive(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:loopthread(message),daemon=True)
    bypass.start()


# doc thread
def docthread(message):
    if message.document.file_name.endswith("dlc"):
        msg = app.send_message(message.chat.id, "🔎 __bypassing...__", reply_to_message_id=message.id)
        print("sent DLC file")
        sess = requests.session()
        file = app.download_media(message)
        dlccont = open(file,"r").read()
        link = bypasser.getlinks(dlccont,sess)
        app.edit_message_text(message.chat.id, msg.id, f'__{link}__')
        os.remove(file)

# doc
@app.on_message(filters.document)
def docfile(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
    bypass = threading.Thread(target=lambda:docthread(message),daemon=True)
    bypass.start()


# server loop
print("Bot Starting")
app.run()
