#!/usr/bin/python3

import time
import traceback
import asyncio
from operator import itemgetter
from http.client import HTTPException
from texttable import Texttable
from ad_extractor import Ad
from ad_manager import AdManager
from desktop_notification_manager import DesktopNotificationManager

URL = (
    'https://hardverapro.hu/aprok/mobil/mobil/keres.php?stext=poco+x3+nfc&stcid_text='
    '&stcid=&stmid_text=&stmid=&minprice=&maxprice=&cmpid_text=&cmpid=&usrid_text=&usrid='
    '&__buying=0&__buying=1&stext_none=')

TIME_BETWEEN_UPDATES = 60*15 # seconds


def print_table(ads_list: list[Ad]) -> None:
    table_rows_list: list[list[str]] = []

    for ad in ads_list:
        table_row: list[str] = []
        table_row.append(ad.title)
        table_row.append(ad.price)
        if ad.is_frozen:
            table_row.append('\n\u2744')  # Add a snowflake if frozen
        else:
            table_row.append('')
        table_row.append(ad.city)
        table_row.append(ad.seller_name)
        table_row.append(ad.seller_rating)
        table_row.append(ad.link)
        table_rows_list.append(table_row)

    # Add header
    header = (
        ['Title',
         'Price',
         'Is It Frozen',
         'City', 'Seller',
         'Seller Rating',
         'Link'])
    table_rows_list.insert(0, header)

    table = Texttable()
    table.set_cols_align(['c', 'r', 'c', 'l', 'l', 'c', 'l'])
    table.set_cols_valign(['m', 'm', 'm', 'm', 'm', 'm', 'm'])
    table.set_cols_width([35, 20, 10, 25, 25, 10, 100])
    table.add_rows(table_rows_list, header=True)

    print(table.draw())


async def main() -> None:
    notification_manager = DesktopNotificationManager()
    ad_manager = AdManager()
    while True:
        try:
            print('Checking for new ads...')
            new_ads = ad_manager.update_ads_and_return_new_ones()
            if new_ads:
                print("New ads has been found:")
                print_table(new_ads)
                notification_manager.send_notifications_about_new_ads(new_ads)
            else:
                print("There were no new ads.")
        except HTTPException:
            print('A network error occurred!')
            traceback.print_exc()

        print('Going back to sleep...')
        print('', flush=True)
        ad_manager.save_ads()
        await asyncio.sleep(TIME_BETWEEN_UPDATES)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Quitting...')
