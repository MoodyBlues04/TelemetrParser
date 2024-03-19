import datetime
from os import getenv
from telethon import TelegramClient


class TgApi:
    def __init__(self):
        self.__client = TelegramClient(
            'telemetr-io-client',
            int(getenv('TG_API_ID')),
            getenv('TG_API_HASH')
        )

    async def is_channel_inactive(self, channel_tag: str, last_activity_expected=None) -> bool:
        if last_activity_expected is None:
            last_activity_expected = datetime.datetime.today() - datetime.timedelta(days=7)

        channel_id = await self.get_channel_id(channel_tag)
        last_message_date = await self.get_last_message_date(channel_id)

        return last_message_date >= last_activity_expected

    async def get_channel_id(self, channel_tag: str) -> int:
        channel = await self.__client.get_entity(channel_tag)
        return channel.id

    async def get_last_message_date(self, channel_id: int) -> datetime.datetime:
        last_date = None
        async for message in self.__client.iter_messages(channel_id, limit=3):
            if last_date is None or last_date < message.date:
                last_date = message.date
        return last_date

