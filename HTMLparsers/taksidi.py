from bs4 import BeautifulSoup
from bs4.element import Comment
import re, datetime, json, requests, os, time,csv
from collections import OrderedDict


i = 0
data = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\taksidi.html', encoding="utf8")

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d")
soup = BeautifulSoup(data, "html.parser")

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

scraped_store_taksidi = []
links = []
freeslot = []
country = []
where = []
price = []
pricepromo = []
date = []

print("TAKSIDI in progress...")
for div in soup.find_all('a', attrs={'class':'trip-single'}):

    i += 1

    div_country = div.find('div','trip-place')
    div_country = div_country.find('p').get_text().strip()
    country.append(div_country)
    # print(div_country)

    div_place_where = div.find('div','trip-desc')
    # print(div_place_where)
    div_place_where = div_place_where.find('h3').get_text().strip()
    # prints the p tag content
    if("@" in div_place_where):
        div_place_where.split(" @ ")[1].strip()
        # print(div_place_where.split(" @ ")[1].strip())
        where.append(div_place_where.split(" @ ")[1].strip())
    else:
        where.append(div_place_where)
        # print(div_place_where)

    div_date = div.find('div','trip-date')
    div_date = div_date.find('p').get_text().strip()
    # print(div_date)
    date.append(div_date)

    div_price_original = div.find('div','trip-price')

    div_price_original = div_price_original.find('p','trip-price-old')
    div_price_promo = div.find('p','trip-price-promo')
    # div_price_promo = div_price_promo.find('p').get_text().strip()

    if(div_price_original is None):
        price.append("none")
        # print("none")
    else:
        # print(div_price_original.get_text().strip())
        price.append(div_price_original.get_text().strip())

    if(div_price_promo is None):
        pricepromo.append("none")
        # print("none")
    else:
        # print(div_price_promo.get_text().strip())
        pricepromo.append(div_price_promo.get_text().strip())

    div_slot = div.find("div", "trip-price-down")
    # print(div_slot)
    # gets 2nd 'p' sibling from parent tag:
    div_slot = div_slot.select("p:nth-of-type(2)")
    if(div_slot):
        # print(div_slot[0].get_text().strip())
        freeslot.append(div_slot[0].get_text().strip())
    else:
        freeslot.append("brak danych")
        # print("brak danych")

    link = div['href']
    link = "https://taksidi.pl" + link
    # print(link)
    links.append(link)

for i, value in enumerate(where):
    store_info = {}

            # if tempDate[i] >= now and tempDate[i] > "2018-12-01":
    store_info = {
                                'Organizator': "TAKSIDI",
                                'City': where[i],
                                'Country': country[i],
                                'Date': date[i],
                                'Price': price[i],
                                'Free slots': freeslot[i],
                                'Link': links[i]

                            }

    print("{0}:\n Gdzie: {1} \n Kraj: {2} \n Kiedy: {3}\n Cena: {4}\n Wolne miejsca: {5}\n Link: {6}".
                              format(i, where[i], country[i], date[i], price[i], freeslot[i], links[i], '\n'))

    scraped_store_taksidi.append(store_info)

# print(scraped_store_taksidi[1])
with open(r'C:\Users\PREZES\Desktop\snowridess\venv\taksidi.csv', 'w', newline='', encoding="utf8") as csvfile:

    for i in range(len(scraped_store_taksidi)):
        # print(scraped_store_taksidi[i]["Country"])
        fieldnames = ['country', 'city', 'Date', 'Price', 'Free slots', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
                        "country": scraped_store_taksidi[i]["Country"],
                         "city": scraped_store_taksidi[i]["City"],
                         "Date": scraped_store_taksidi[i]["Date"],
                         "Price": scraped_store_taksidi[i]["Price"],
                         "Free slots": scraped_store_taksidi[i]["Free slots"],
                         "Link": scraped_store_taksidi[i]["Link"]
                         })

# print("temp.csv created successfully")
