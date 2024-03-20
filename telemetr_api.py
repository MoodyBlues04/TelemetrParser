from telethon import TelegramClient
import datetime
import sys
import pytz
from dotenv import load_dotenv
from os import getenv

load_dotenv('.env')

utc = pytz.UTC


class TgApi:
    def __init__(self):
        self.__client = TelegramClient(
            'telemetr-io-client',
            int(getenv('TG_API_ID')),
            getenv('TG_API_HASH')
        )

    @property
    def client(self):
        return self.__client

    async def is_channel_inactive(self, channel_tag: str, last_activity_expected=None) -> bool:
        if last_activity_expected is None:
            last_activity_expected = datetime.datetime.now() - datetime.timedelta(days=7)

        channel_id = await self.get_channel_id(channel_tag)
        last_message_date = await self.get_last_message_date(channel_id)

        last_activity_expected = utc.localize(last_activity_expected)

        return last_message_date < last_activity_expected

    async def get_channel_id(self, channel_tag: str) -> int:
        channel = await self.__client.get_entity(channel_tag)
        return channel.id

    async def get_last_message_date(self, channel_id: int) -> datetime.datetime:
        last_date = None
        async for message in self.__client.iter_messages(channel_id, limit=3):
            if last_date is None or last_date < message.date:
                last_date = message.date
        return last_date


api = TgApi()


async def main():
    print(int(await api.is_channel_inactive(sys.argv[1])), end="")
    exit(0)

with api.client:
    api.client.loop.run_until_complete(main())
