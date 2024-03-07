from os import getenv
from django.core.management.base import BaseCommand
from app.services.facades import TelemetrParsingFacade


class Command(BaseCommand):
    help = "Parses telemetr.io website."

    def handle(self, *args, **options):
        TelemetrParsingFacade(getenv('SHEET_ID')).parse_telemetr_to_sheets()
