from telethon import TelegramClient, events
import json

import DB

api_id = ''
api_hash = ''
name = "gbtest"


class TelegramParser:
    def __init__(self, chat_title):
        self.api_id = ''
        self.api_hash = ''
        self.chat_title=chat_title
        with open(file="./credentials.json") as f:
            data = json.load(f)
            self.api_id = data['api_id']
            self.api_hash = data['api_hash']
        self.start(self.chat_title)

        # @client.on(events.NewMessage)
        # async def event_handler(event):
        #     chat = await event.get_chat()
        #     sender = await event.get_sender()
        #     chat_id = await event.chat_id
        #     sender_id = await event.sender_id
        #     sender_name = await sender.get_display_name()
        #     entity = await client.get_entity(sender_id)

    def start(self, chat_title):
        self.client = TelegramClient('mysession', self.api_id, self.api_hash)
        with self.client:
            self.client.loop.run_until_complete(self.getUsersFromChat(chat_title))

    async def getUsersFromChat(self,chat_title):
        users = []
        members=[]
        dialogs = await self.client.get_dialogs(limit=10)
        for dialog in dialogs:
            if dialog.title == chat_title:
                members = await self.client.get_participants(dialog)
        for member in members:
            users.append({
                'name': member.first_name,
                'surname': member.last_name,
                'id': member.id,
                'username': member.username,
                'phone': member.phone,
            })

        # add to database
        DB.insertIntoMongoDB(users)
        return users
