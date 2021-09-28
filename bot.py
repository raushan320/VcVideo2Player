from config import Config
from pyrogram import Client

bot = Client(
    "VcVideoPlayer",
    Config.API_ID,
    Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="player")
)
