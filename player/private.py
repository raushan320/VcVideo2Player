import os
import sys
import asyncio
from config import Config
from helpers.logger import LOGGER
from helpers.utils import update, is_admin
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument


HOME_TEXT = "🎉 **Wtsup [{}](tg://user?id={})**, \n\nI Am **VcVideoPlayer**. \n`Lets Enjoy Cinematic View  of Group Video Player With Your Friends ❤️😊` \n\n**Made With 💞 By @TeamDeeCode!**"
HELP_TEXT = """
🍃 --**SETTINGS**-- :

\u2022 `Add me to your group and my assistant too make admin both!`
\u2022 `Start a voice chat in your group & Restart the boy if not join to vc.`
\u2022 `Try /stream [video name] and /stream reply to amy video and yt link!`

🍃 --**COMMANDS**-- :

\u2022 `/seek` - seek the video
\u2022 `/skip` - skip current video
\u2022 `/live` - start live stream
\u2022 `/pause` - pause playing video
\u2022 `/resume` - resume playing video
\u2022 `/mute` - mute the vc userbot
\u2022 `/unmute` - unmute the vc userbot
\u2022 `/leave` - leave the voice chat
\u2022 `/shuffle` - shuffle the playlist
\u2022 `/volume` - change volume (0-200)
\u2022 `/replay` - play from the beginning
\u2022 `/clear` - clear the playlist queue
\u2022 `/restart` - update & restart the bot
\u2022 `/setvar` - set/change heroku configs
\u2022 `/getlogs` - get the ffmpeg & bot logs

© **Powered By** : 
**@TeamDeeCoDe** 👩‍💻
"""

admin_filter=filters.create(is_admin) 

@Client.on_message(filters.command(["start", f"start@{Config.BOT_USERNAME}"]))
async def start(client, message):
    if message.chat.type == 'private':
        buttons = [
            [
                InlineKeyboardButton("Sᴇᴀʀᴄʜ", switch_inline_query_current_chat=""),
            ],
            [
                InlineKeyboardButton("Cʜᴀɴɴᴇʟ", url="https://t.me/DeeCodeBots"),
                InlineKeyboardButton("Gʀᴏᴜᴘ", url="https://t.me/DeCodeSupport"),
            ],
            [
                InlineKeyboardButton("Bᴏᴛ Lɪꜱᴛ", url="https://t.me/otherBotList"),
                InlineKeyboardButton("Sᴏᴜʀᴄᴇ", url="https://github.com/TeamDeeCode/VcVideoPlayer/tree/alpha"),
            ],
            [
                InlineKeyboardButton("Hᴇʟᴘ & Cᴏᴍᴍᴀɴᴅꜱ", callback_data="help"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(HOME_TEXT.format(message.from_user.first_name, message.from_user.id), reply_markup=reply_markup)
    else:
        await message.reply_text(f"**🌟 I'm Alive 🔥**")

@Client.on_message(filters.command(["help", f"help@{Config.BOT_USERNAME}"]))
async def show_help(client, message):
    if message.chat.type == 'private':
        buttons = [
            [
                InlineKeyboardButton("Cʟᴏꜱᴇ", callback_data="close"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        if Config.msg.get('help') is not None:
            await Config.msg['help'].delete()
        Config.msg['help'] = await message.reply_text(
            HELP_TEXT,
            reply_markup=reply_markup
            )
    else:
        await message.reply_text(
            "**Contact me in PM to get a List of Commands ✨**", 
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Hᴇʟᴘ ❔", url=f"http://t.me/{Config.BOT_USERNAME}?start=help")
                    ]
                ]
            )
        )


@Client.on_message(filters.command(["restart", "update", f"restart@{Config.BOT_USERNAME}", f"update@{Config.BOT_USERNAME}"]) & admin_filter)
async def update_handler(client, message):
    if Config.HEROKU_APP:
        k=await message.reply_text("✨ **Heroku Detected, \nRestarting Your App!**")
    else:
        k=await message.reply_text("🔄 **Processing...**")
    await update()
    try:
        await k.edit("🎉 **Restarted Successfully!**")
    except:
        pass


@Client.on_message(filters.command(["getlogs", f"getlogs@{Config.BOT_USERNAME}"]) & admin_filter)
async def get_logs(client, message):
    logs=[]
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("ffmpeg.txt", caption="FFMPEG Logs"))
    if os.path.exists("ffmpeg.txt"):
        logs.append(InputMediaDocument("botlog.txt", caption="Video Player Logs"))
    if logs:
        try:
            await message.reply_media_group(logs)
        except:
            await message.reply_text("❌ **An Error Occurred !**")
            pass
        logs.clear()
    else:
        await message.reply_text("❌ **No Logs File Find !**")


@Client.on_message(filters.command(["setvar", f"setvar@{Config.BOT_USERNAME}"]) & admin_filter)
async def set_heroku_var(client, message):
    if not Config.HEROKU_APP:
        buttons = [[InlineKeyboardButton('HEROKU_API_KEY', url='https://dashboard.heroku.com/account/applications/authorizations/new')]]
        await message.reply_text(
            text="❗ **No Heroku App Found !** \n__Please Note That, This Command Needs The Following Heroku Vars To Be Set :__ \n\n1. `HEROKU_API_KEY` : Your heroku account api key.\n2. `HEROKU_APP_NAME` : Your heroku app name. \n\n**For More Ask In @DeCodeSupport !!**", 
            reply_markup=InlineKeyboardMarkup(buttons))
        return     
    if " " in message.text:
        cmd, env = message.text.split(" ", 1)
        if  not "=" in env:
            return await message.reply_text("❗ **You Should Specify The Value For Variable!** \n\nFor Example: \n`/setvar CHAT_ID=-1001173097859`")
        var, value = env.split("=", 2)
        config = Config.HEROKU_APP.config()
        if not value:
            m=await message.reply_text(f"❗ **No Value Specified, So Deleting `{var}` Variable !**")
            await asyncio.sleep(2)
            if var in config:
                del config[var]
                await m.edit(f"🗑 **Sucessfully Deleted `{var}` !**")
                config[var] = None
            else:
                await m.edit(f"🤷‍♂️ **Variable Named `{var}` Not Found, Nothing Was Changed !**")
            return
        if var in config:
            m=await message.reply_text(f"⚠️ **Variable Already Found, So Edited Value To `{value}` !**")
        else:
            m=await message.reply_text(f"⚠️ **Variable Not Found, So Setting As New Var !**")
        await asyncio.sleep(2)
        await m.edit(f"🎉 **Succesfully Set Variable `{var}` With Value `{value}`, Now Restarting To Apply Changes !**")
        config[var] = str(value)
    else:
        await message.reply_text("❗ **You Haven't Provided Any Variable, You Should Follow The Correct Format !** \n\nFor Example: \n• `/setvar CHAT_ID=-1001173097859` to change or set CHAT_ID var. \n• `/setvar REPLY_MESSAGE=` to delete REPLY_MESSAGE var.") 
