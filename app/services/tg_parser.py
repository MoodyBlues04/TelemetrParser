from bs4 import BeautifulSoup
from requests import get
from datetime import datetime, timedelta
import pytz


class TgParser:
    def __init__(self):
        self.__utc = pytz.UTC

    def is_active(self, preview_link: str, last_activity_expected=None) -> bool:
        if last_activity_expected is None:
            last_activity_expected = datetime.now() - timedelta(days=7)

        message_dates = self.get_message_dates(preview_link)
        last_date = max(message_dates)

        last_activity_expected = self.__utc.localize(last_activity_expected)

        return last_date >= last_activity_expected

    def get_message_dates(self, url) -> list[datetime]:
        page = self.__get_page(url)

        bs = BeautifulSoup(page, "html.parser")
        date_elements = bs.findAll('a', {'class': 'tgme_widget_message_date'})
        dates = []

        for date_element in date_elements:
            date = date_element.find('time').get('datetime')
            date = date[:10]
            dates.append(datetime.strptime(date, '%Y-%m-%d'))

        return dates

    def __get_page(self, url: str) -> str:
        return get(url).text
