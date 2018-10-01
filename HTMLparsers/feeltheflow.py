#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request, re, json
from collections import OrderedDict

i = 1
data = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\feeltheflow.html', encoding="utf8")

soup = BeautifulSoup(data, "html.parser")
scraped_store_feeltheflow = []

print("FEELTHEFLOW in progres...")
try:
    for div in soup.find_all("div", attrs={'class': re.compile("^offer row")}):

        # for i, n in enumerate(div):
        #    print(i,": ",n)

        # div_where = div.find('span', attrs={'class': re.compile("^city-")}).get_text().strip() # ^city-[a-z]+
        div_wheree = div.find('span', class_='city-country')
        # print(t.get_text("|", strip=True))
        div_where = [text for text in div_wheree.stripped_strings][0].strip()
        # # #
        div_country = [text for text in div_wheree.stripped_strings][1].strip()
        # # #
        div_pricee = div.find('span', attrs={'class': 'price'}).get_text().strip()
        div_price = [y for y in (div.strip() for div in div_pricee.splitlines()) if y][0]
        # # #
        div_date = div.find('span', attrs={'class': 'date text-orange'}).get_text().strip()
        # div_dte = re.match('(\d\d.\d\d.\d\d\d\d)(?:\s\s+)( - \d\d.\d\d.\d\d\d\d)', div_place_date)
        # div_date = div_dte.group(1)+div_dte.group(2)
        # # #
        link = div.find('a')['href']
        # # #
        try:
            last_slots = div.find('div', attrs={'class': 'promo-box'}).get_text().strip()
        except AttributeError as err:
            last_slots = ("SĄ WOLNE MIEJSCA")
        # # #
        # print("{0}:\n Gdzie: {1} \n Kraj: {2} \n Kiedy: {3}\n Cena: {4}\n Link: {5}\n Wolne miejsca: {6}".
        #       format(i, div_where, div_country, div_date, div_price, link, last_slots, '\n'))

        # print(i , last_slots," | " + div_place_where + " | ", div_price, div_place_date,link)
        i += 1

        store_info = {}
        store_info = {
            'Organizator': "FEELTHEFLOW",
            'City': div_where,
            'Country': div_country,
            'Date': div_date,
            'Price': div_price,
            'Free slots': last_slots,
            'Link': link

        }

        scraped_store_feeltheflow.append(store_info)
except IOError as e:
    print("FEELTHEFLOW Errors: I/O error({0}): {1}".format(e.errno, e.strerror))
print("FEELTHEFLOW done")
#
# with open(r'feeltheflow.json', 'w', encoding="utf8") as json_file:
#     json.dump(scraped_store_feeltheflow, json_file, indent=4,ensure_ascii=False)
