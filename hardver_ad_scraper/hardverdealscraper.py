# My simple messy script to get all ads from a harverapro link
# By Ádám Madar

import json
from typing import Any
from urllib.request import urlopen
from bs4 import BeautifulSoup, Tag
from .ad import Ad, AdJSONDecoder, AdJSONEncoder


class DealExtractor:
    """A simple class to get all the deals from a hardverapro.hu link"""

    def __init__(self, url: str) -> None:
        self.__url: str = url

    def get_ads(self) -> list[Ad]:
        content = urlopen(self.__url).read()
        soup = BeautifulSoup(content, features='html.parser')
        ad_container = soup.find('div', attrs={'class': 'uad-list'})
        ads_list: list[Ad] = []

        # Return if there is no data to process
        if not isinstance(ad_container, Tag):
            return []

        rows = ad_container.find_all(attrs={'class': 'media-body'})
        for row in rows:
            # If it's a sponsored ad
            if 'featured' in row.parent['class']:
                # Then skip it
                continue

            # Note: something(...) is equal to something.find_all(...)!
            title_col = row.find(attrs={'class': 'uad-title'})
            title = title_col.a.text.strip()
            link = title_col.a['href'].strip()
            is_frozen = False
            if title_col.p:
                is_frozen = True

            info_col = row.find(attrs={'class': 'uad-info'})
            price = info_col.find(attrs={'class': 'uad-price'}).text.strip()
            city = info_col.find(attrs={'class': 'uad-light'}).text.strip()

            misc_col = row.find(attrs={'class': 'uad-misc'})
            seller_data = misc_col.find_all(attrs={'class': 'uad-light'})
            seller_name = seller_data[0].a.text.strip()
            seller_rating = seller_data[1].span.text.strip()

            ad = Ad(
                title=title,
                link=link,
                price=price,
                is_frozen=is_frozen,
                city=city,
                seller_name=seller_name,
                seller_rating=seller_rating,
            )
            ads_list.append(ad)

        return ads_list
