import os 
import asyncio
from bot import bot
from pyrogram import idle
from config import Config
from helpers.logger import LOGGER
from pmpermit.user import group_call
from helpers.utils import start_stream


if not os.path.isdir("./downloads"):
    os.makedirs("./downloads")
else:
    for f in os.listdir("./downloads"):
        os.remove(f"./downloads/{f}")

async def main():
    await bot.start()
    Config.BOT_USERNAME = (await bot.get_me()).username
    await group_call.start()
    await start_stream()
    LOGGER.warning(f"{Config.BOT_USERNAME} Started Successfully !")
    await idle()
    LOGGER.warning("VcVideoPlayer Stopped !")
    await group_call.start()
    await bot.stop()

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())


