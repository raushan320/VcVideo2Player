from config import Config
from helpers.logger import LOGGER
from pyrogram import Client
from pytgcalls import PyTgCalls

USER = Client(
    Config.SESSION,
    Config.API_ID,
    Config.API_HASH,
    plugins=dict(root="pmpermit")
    )
group_call = PyTgCalls(USER, cache_duration=180)
