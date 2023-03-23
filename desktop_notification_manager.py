import desktop_notify
import asyncio
from ad_extractor import Ad
from dbus_next.signature import Variant
import webbrowser


class DesktopNotificationManager:
    def __init__(self) -> None:
        pass

    def send_notifications_about_new_ads(self, ads: list[Ad]):
        for ad in ads:
            server = desktop_notify.aio.Server('Hardverapro Dealwatch')
            notification = server.Notify(
                ad.title,
                f'From: {ad.seller_name}; Price: {ad.price}; Seller Rating: {ad.seller_rating}\n<a href="{ad.link}">Link to the ad</a>')

            # What are these Variants? See here: https://python-dbus-next.readthedocs.io/en/latest/type-system/index.html
            notification.set_hint('sound-name', Variant('s', 'message-new-instant'))
            notification.set_hint('category', Variant('s', 'im.received'))
            notification.set_hint('urgency', Variant('y', 2))
            notification.set_hint('urgency', Variant('y', 2))

            notification.ad_link = ad.link
            notification.add_action(desktop_notify.Action('Open in browser', lambda notification: webbrowser.open(notification.ad_link)))

            asyncio.create_task(notification.show())
