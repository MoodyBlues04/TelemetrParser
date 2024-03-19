from __future__ import annotations

import time
from os import getenv
import requests
from bs4 import BeautifulSoup
from app.models import ParsedChannel
from .dto import TableRow
from .tg_api import is_channel_inactive


class TelemetrParser:
    def __init__(self, category: str) -> None:
        self.__category = category

    def parse(self) -> list[TableRow]:
        channels_iterator = TelemetrChannelsIterator(category=self.__category)

        parsed_rows = []
        for page_index, page in enumerate(channels_iterator):
            print(f"Parsing page: {page_index}")

            bs = BeautifulSoup(page, "html.parser")
            tbody = bs.find('tbody')
            table_rows = tbody.findAll('tr')

            for row_idx, table_row in enumerate(table_rows):
                if row_idx % 10 == 0:
                    print(f"Row index: {row_idx}/{len(table_rows)}")
                row_cells = table_row.findAll('td')
                parsed_row = self.__make_parsed_row(row_cells)
                if ParsedChannel.row_updated(parsed_row):
                    parsed_rows.append(parsed_row)

            time.sleep(2) # for tg api not to fail

        return parsed_rows

    def __make_parsed_row(self, row_cells: list) -> TableRow:
        parsed_row = TableRow()
        try:
            name_attr = row_cells[1].find('div', class_='channel-name__attribute')
            channel_tag = name_attr.text
            print(name_attr.find('a'))
            exit(0)
            if channel_tag != 'Канал закрыт':
                is_inactive = is_channel_inactive(channel_tag)
                status = TableRow.STATUS_INACTIVE if is_inactive else TableRow.STATUS_ACTIVE
            else:
                status = TableRow.STATUS_CLOSED

            parsed_row.index = self.__parse_int(row_cells[0].text)
            parsed_row.status = status
            parsed_row.name = row_cells[1].find('a', class_='channel-name__title').text.strip()
            parsed_row.image = row_cells[1].find('img', class_='avatar').get('src')
            parsed_row.subscribers = self.__parse_int(row_cells[2].find('span').text)
            parsed_row.increment = self.__parse_int(row_cells[3].text)
            if row_cells[3].find('i', class_='icon-carret-down-line') is not None:
                parsed_row.increment *= -1
            parsed_row.post_views = self.__parse_int(row_cells[4].text)
            parsed_row.er = self.__parse_float(row_cells[5].text)
            parsed_row.references = self.__parse_int(row_cells[6].text)
            parsed_row.geo = row_cells[7].text.strip()
            parsed_row.category = row_cells[8].text.strip()
            return parsed_row
        except Exception as e:
            print(e)
            return parsed_row

    def __parse_int(self, text: str) -> int:
        return int(text.replace(' ', ''))

    def __parse_float(self, text: str) -> float:
        return float(self.__replace_many(text, [' ', '%'], ''))

    def __replace_many(self, text: str, target: list[str], replacement: str) -> str:
        res = text
        for replace_ch in target:
            res = res.replace(replace_ch, replacement)
        return res


class TelemetrApi:
    __BASE_URL = 'https://telemetr.io/ru'

    CATEGORY_CRYPTO = '7JeRWunw9'
    COUNTRY_RUS = 'russia'

    def __init__(self) -> None:
        self.__proxy = dict()
        if getenv('PROXY_HOST') is not None:
            self.__proxy = {
                'https': self.__make_proxy_url_from_env()
            }

    def get_channels_page(self, category: str = CATEGORY_CRYPTO, country: str = COUNTRY_RUS, page: int = 1) -> str:
        """ Returns webpage with tg channels data """
        url = f'{self.__BASE_URL}/category/{category}?countries={country}&sort=participants_count&page={page}'
        return self.__get(url).text

    def __get(self, url: str) -> requests.Response:
        return requests.get(url, proxies=self.__proxy)

    def __make_proxy_url_from_env(self) -> str:
        return f"http://{getenv('PROXY_USER')}:{getenv('PROXY_PASSWORD')}@{getenv('PROXY_HOST')}:{getenv('PROXY_PORT')}"


class TelemetrChannelsIterator:
    MAX_PAGE = 10

    def __init__(
            self,
            category: str = TelemetrApi.CATEGORY_CRYPTO,
            country: str = TelemetrApi.COUNTRY_RUS,
            page: int = 1) -> None:
        self.__category = category
        self.__country = country
        self.__page = page
        self.__api = TelemetrApi()

    def __iter__(self) -> TelemetrChannelsIterator:
        return self

    def __next__(self) -> str:
        if self.__page > self.MAX_PAGE:
            raise StopIteration

        page_html = self.__api.get_channels_page(self.__category, self.__country, self.__page)
        self.__page += 1
        return page_html
