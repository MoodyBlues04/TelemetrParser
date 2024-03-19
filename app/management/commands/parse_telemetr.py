import asyncio
from os import getenv
from django.core.management.base import BaseCommand
from app.services.facades import TelemetrParsingFacade



import pytz
from telethon import TelegramClient
from django.conf import settings
import datetime
utc = pytz.UTC


class TgApi:
    def __init__(self):
        self.__client = TelegramClient(
            str(settings.BASE_DIR) + '/telemetr-io-client',
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


api = TgApi()

class Command(BaseCommand):
    help = "Parses telemetr.io website."

    def add_arguments(self, parser):
        parser.add_argument('--sheet_id', type=str, help="Google sheet id to parse to")
        parser.add_argument('--category', type=str, help="Telemetr.io category to parse from")

    def handle(self, *args, **options):
        print(asyncio.run(api.is_channel_inactive('new_ton_news')))
        # self.__validate_options(options)
        #
        # sheet_id = options.get('sheet_id', getenv('SHEET_ID'))
        # category = options.get('category')

        # TelemetrParsingFacade(sheet_id, category).parse_telemetr_to_sheets()

    def __validate_options(self, options: dict) -> None:
        required_options = ['category', 'sheet_id']
        for option in required_options:
            if options.get(option) is None:
                raise Exception(f'Invalid args: {option} field is required')
