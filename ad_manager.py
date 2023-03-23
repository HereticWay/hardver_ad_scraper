from os import path
import json
from ad_extractor import AdExtractor, Ad, AdJSONEncoder

ADS_FILE = './ads.json'
URL = (
    'https://hardverapro.hu/aprok/mobil/mobil/keres.php?stext=poco+x3+nfc&stcid_text='
    '&stcid=&stmid_text=&stmid=&minprice=&maxprice=&cmpid_text=&cmpid=&usrid_text=&usrid='
    '&__buying=0&__buying=1&stext_none=')


class AdManager:
    __slots__ = (
        'ads',
        'ad_extractor'
    )

    def __init__(self) -> None:
        self.ads = self.load_ads() or []
        self.ad_extractor = AdExtractor(url=URL)

    def load_ads(self) -> list[Ad] | None:
        if not path.exists(ADS_FILE):
            return None

        ads: list[Ad] = []
        with open(ADS_FILE, 'r') as file:
            for ad_dict in json.loads(file.read()):
                ads.append(Ad(**ad_dict))
        return ads

    def save_ads(self) -> None:
        with open(ADS_FILE, 'w') as file:
            file.write(json.dumps(self.ads, cls=AdJSONEncoder, indent=4))

    def update_ads_and_return_new_ones(self) -> list[Ad]:
        ads = self.ad_extractor.get_ads()

        new_ads: list[Ad] = [ad for ad in ads if ad not in self.ads]
        self.ads = ads

        return new_ads

