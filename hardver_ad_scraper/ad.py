import json
from typing import Any


class Ad:
    # __slots__ = (
    #     'title',
    #     'link',
    #     'price',
    #     'is_frozen',
    #     'city',
    #     'seller_name',
    #     'seller_rating'
    # )

    def __init__(self, title: str, image_url: str, link: str, price: str, is_frozen: bool, city: str, seller_name: str, seller_rating_positive: str, seller_rating_negative: str) -> None:
        self.title = title
        self.image_url = image_url
        self.link = link
        self.price = price
        self.is_frozen = is_frozen
        self.city = city
        self.seller_name = seller_name
        self.seller_rating_positive = seller_rating_positive
        self.seller_rating_negative = seller_rating_negative

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ad):
            return (
                self.title == other.title and
                self.image_url == other.image_url and
                self.link == other.link and
                self.price == other.price and
                self.is_frozen == other.is_frozen and
                self.city == other.city and
                self.seller_name == other.seller_name)
                # self.seller_rating_positive == other.seller_rating_positive and
                # self.seller_rating_negative == other.seller_rating_negative)

        return False


class AdJSONEncoder(json.JSONEncoder):
    def default(self, obj: Ad) -> dict[str, Any]:
        if isinstance(obj, Ad):
            return {
                'title': obj.title,
                'image_url': obj.image_url,
                'link': obj.link,
                'price': obj.price,
                'is_frozen': obj.is_frozen,
                'city': obj.city,
                'seller_name': obj.seller_name,
                'seller_rating_positive': obj.seller_rating_positive,
                'seller_rating_negative': obj.seller_rating_negative
            }
        else:
            return super().default(obj)


class AdJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        return Ad(
            obj['title'],
            obj['image_url'],
            obj['link'],
            obj['price'],
            obj['is_frozen'],
            obj['city'],
            obj['seller_name'],
            obj['seller_rating_positive'],
            obj['seller_rating_negative'])
