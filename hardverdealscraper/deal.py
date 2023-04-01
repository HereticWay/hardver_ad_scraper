import json


class Deal:
    __slots__ = (
        'title',
        'link',
        'price',
        'is_frozen',
        'city',
        'seller_name',
        'seller_rating'
    )

    def __init__(self, title: str, link: str, price: str, is_frozen: bool, city: str, seller_name: str, seller_rating: str) -> None:
        self.title = title
        self.link = link
        self.price = price
        self.is_frozen = is_frozen
        self.city = city
        self.seller_name = seller_name
        self.seller_rating = seller_rating

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Deal):
            return self.link == __o.link

        return False


class DealJSONEncoder(json.JSONEncoder):
    def default(self, obj: Deal) -> dict[str, Any]:
        if isinstance(obj, Deal):
            return {
                'title': o.title,
                'link': o.link,
                'price': o.price,
                'is_frozen': o.is_frozen,
                'city': o.city,
                'seller_name': o.seller_name,
                'seller_rating': o.seller_rating
            }
        else:
            return super().default(obj)


class DealJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, obj):
        return Deal(
            obj['title'],
            obj['link'],
            obj['price'],
            obj['is_frozen'],
            obj['city'],
            obj['seller_name'],
            obj['seller_rating'])