from app.services.parser import *
from app.services.google_sheets import *
from datetime import datetime
from app.models import ParsedChannel


class TelemetrParsingFacade:
    def __init__(self, sheet_id: str) -> None:
        self.__google_sheets_api = GoogleSheetsApi(sheet_id, self.__worksheet_title())
        self.__parser = TelemetrParser()

    def parse_telemetr_to_sheets(self) -> None:
        table_rows = self.__parser.parse()
        ParsedChannel.add_rows(table_rows)

        print(f"Total rows parsed: {len(table_rows)}")

        self.__set_sheet_headers()
        self.__set_sheet_data(table_rows)

    def __set_sheet_headers(self) -> None:
        self.__google_sheets_api.set_row(1, self.__sheet_headers())

    def __set_sheet_data(self, table_rows: list[TableRow]) -> None:
        table_data = list(map(lambda table_row: table_row.to_array(), table_rows))
        self.__google_sheets_api.add_rows(table_data)

    def __sheet_headers(self) -> list:
        return [
            'Индекс',
            'Название',
            'Подписчики',
            'Прирост (7d)',
            'Просмотры поста',
            'ER',
            'Упоминания (7d)',
            'ГЕО',
            'Категория',
        ]

    def __worksheet_title(self) -> str:
        return datetime.today().strftime('%Y-%m-%d')
