from helpers.logger import LOGGER
from config import Config
from pyrogram import Client, filters
from pyrogram.errors import BotInlineDisabled

async def is_reply(_, client, message):
    if Config.REPLY_MESSAGE:
        return True
    else:
        return False

reply_filter=filters.create(is_reply)

@Client.on_message(reply_filter & filters.private & filters.incoming & ~filters.bot & ~filters.service & ~filters.me & ~filters.chat([777000, 454000]))
async def nopm(client, message):
    try:
        inline = await client.get_inline_bot_results(Config.BOT_USERNAME, "SAMMY")
        m=await client.send_inline_bot_result(
            message.chat.id,
            query_id=inline.query_id,
            result_id=inline.results[0].id,
            hide_via=True
            )
        old=Config.msg.get(message.chat.id)
        if old:
            await client.delete_messages(message.chat.id, [old["msg"], old["s"]])
        Config.msg[message.chat.id]={"msg":m.updates[1].message.id, "s":message.message_id}
    except BotInlineDisabled:
        LOGGER.error(f"Inline Mode for @{Config.BOT_USERNAME} is not enabled. Enable from @Botfather to enable PM Permit !")
        await message.reply_text(f"{Config.REPLY_MESSAGE}\n\n<b>© Powered By : \n@TeamDeCoDe 👩‍💻</b>")
    except Exception as e:
        LOGGER.error(e)
        pass
