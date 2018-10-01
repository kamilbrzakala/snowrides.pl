from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request, re, json
from datetime import datetime
from collections import OrderedDict

i = 1
data = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\snowz.html', encoding="utf8")

scraped_store_snowz = []
soup = BeautifulSoup(data, "html.parser")


print("SNOWZ in progress...")
try:
    for div in soup.find_all("div", attrs={'class': 'row offer is-flex '}):
        # for i, n in enumerate(div):
        #    print(i,": ",n)
        try:
            div_where = div.find('span', attrs={'class': 'text-left '}).get_text(" ", strip=True).split(" / ")[1]
        except IOError as e:
            print("snowz  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))
        # # #
        try:
            div_country = div.find('span', attrs={'class': 'text-left '}).get_text(" ", strip=True).split(" / ")[0]
        except IOError as e:
            print("snowz  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))
        # # #
        try:
            div_price = div.find('span', attrs={'class': 'promo-price'}).get_text().strip()
        except IOError as e:
            print("snowz  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))
        # # #
        try:
            div_date = div.find('span', attrs={'class': 'text-primary text-left'}).get_text().strip()
        except IOError as e:
            print("snowz  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

        # # #
        try:
            link = "http://snowz.pl"+div.find('a')['href']
        except IOError as e:
            print("snowz  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

        # # #
        try:
            free_slots = div.find('div', attrs={'class': ' btn btn-sm btn-danger mb-1'}).get_text().strip()
        except AttributeError as err:
            try:
                free_slots = div.find('div', attrs={'class': ' btn btn-sm btn-warning mb-1'}).get_text().strip()
            except AttributeError as err:
                free_slots = ("SĄ WOLNE MIEJSCA")

        # # #

        store_info = {}
        store_info = {
            'Organizator': "SNOWZ",
            'City': div_where,
            'Country': div_country,
            'Date': div_date,
            'Price': div_price,
            'Free slots': free_slots,
            'Link': link

        }


        i += 1
        if not div_date.split(" - ")[1] < datetime.now().strftime("%d-%m-%Y"):
            scraped_store_snowz.append(store_info)
            # print("{0}:\n Gdzie: {1} \n Kraj: {2} \n Kiedy: {3}\n Cena: {4}\n Wolne Miejsca: {5} \n Link: {6}".
            #       format(i, div_where, div_country, div_date, div_price, free_slots, link + '\n'))

except IOError as e:
    print("snowz  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))


print("SNOWZ done")
    # poniżej otwieram plik json
# with open('snowz.json', 'w') as json_file:
#     json.dump(scraped_store_snowz, json_file, indent=4, ensure_ascii=False)
