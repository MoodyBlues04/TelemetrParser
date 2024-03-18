from os import getenv
from django.core.management.base import BaseCommand
from app.services.facades import TelemetrParsingFacade


class Command(BaseCommand):
    help = "Parses telemetr.io website."

    def add_arguments(self, parser):
        parser.add_argument('--sheet_id', type=str, help="Google sheet id to parse to")
        parser.add_argument('--category', type=str, help="Telemetr.io category to parse from")

    def handle(self, *args, **options):
        self.__validate_options(options)

        sheet_id = options.get('sheet_id', getenv('SHEET_ID'))
        category = options.get('category')

        TelemetrParsingFacade(sheet_id, category).parse_telemetr_to_sheets()

    def __validate_options(self, options: dict) -> None:
        required_options = ['category', 'sheet_id']
        for option in required_options:
            if options.get(option) is None:
                raise Exception(f'Invalid args: {option} field is required')
