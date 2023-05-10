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

    def __init__(self, title: str, link: str, price: str, is_frozen: bool, city: str, seller_name: str, seller_rating: str) -> None:
        self.title = title
        self.link = link
        self.price = price
        self.is_frozen = is_frozen
        self.city = city
        self.seller_name = seller_name
        self.seller_rating = seller_rating

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Ad):
            return (
                self.title == other.title and
                self.link == other.link and
                self.price == other.price and
                self.is_frozen == other.is_frozen and
                self.city == other.city and
                self.seller_name == other.seller_name and
                self.seller_rating == other.seller_rating)

        return False


class AdJSONEncoder(json.JSONEncoder):
    def default(self, obj: Ad) -> dict[str, Any]:
        if isinstance(obj, Ad):
            return {
                'title': obj.title,
                'link': obj.link,
                'price': obj.price,
                'is_frozen': obj.is_frozen,
                'city': obj.city,
                'seller_name': obj.seller_name,
                'seller_rating': obj.seller_rating
            }
        else:
            return super().default(obj)


class AdJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        return Ad(
            obj['title'],
            obj['link'],
            obj['price'],
            obj['is_frozen'],
            obj['city'],
            obj['seller_name'],
            obj['seller_rating'])
