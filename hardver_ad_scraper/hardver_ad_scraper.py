from typing import Any
from urllib.request import urlopen
from bs4 import BeautifulSoup, Tag
from .ad import Ad


class HardverAdScraper:
    """A simple class to scrape all the ads from a hardverapro.hu link"""

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

        rows = ad_container.find_all(attrs={'class': 'media'})
        for row in rows:
            # If it's a sponsored ad
            if 'featured' in row['class']:
                # Then skip it
                continue

            image_url = f'https:{row.img["data-retina-url"]}'

            row_body = row.find(attrs={'class': 'media-body'})

            # Note: something(...) is equal to something.find_all(...)!
            title_col = row_body.find(attrs={'class': 'uad-title'})
            title = title_col.a.text.strip()
            link = title_col.a['href'].strip()
            is_frozen = False
            if title_col.p:
                is_frozen = True

            info_col = row_body.find(attrs={'class': 'uad-info'})
            price = info_col.find(attrs={'class': 'uad-price'}).text.strip()
            city = info_col.find(attrs={'class': 'uad-light'}).text.strip()

            misc_col = row_body.find(attrs={'class': 'uad-misc'})
            seller_data = misc_col.find_all(attrs={'class': 'uad-light'})
            seller_name = seller_data[0].a.text.strip()
            positive_rating_span = seller_data[1].find(attrs={'class': 'uad_rating_positive'})
            negative_rating_span = seller_data[1].find(attrs={'class': 'uad_rating_negative'})
            seller_rating_positive = positive_rating_span.text.strip() if positive_rating_span else 'N.A.'
            seller_rating_negative = negative_rating_span.text.strip() if negative_rating_span else 'N.A.'

            ad = Ad(
                title=title,
                image_url=image_url,
                link=link,
                price=price,
                is_frozen=is_frozen,
                city=city,
                seller_name=seller_name,
                seller_rating_positive=seller_rating_positive,
                seller_rating_negative=seller_rating_negative
            )
            ads_list.append(ad)

        return ads_list
