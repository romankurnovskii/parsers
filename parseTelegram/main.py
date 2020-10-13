import asyncio

import DB
from telegram import TelegramParser

chat_title = 'React — русскоговорящее сообщество'
parser = TelegramParser(chat_title=chat_title)
# async def start():
#     users = await parser.start()
#     print(users)
#     return users
#
# asyncio.run(start())

# DB.insertHeadhunter(users)
