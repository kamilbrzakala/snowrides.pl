from bs4 import BeautifulSoup
from bs4.element import Comment
import re, datetime, json, requests, os, time
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
date = []
tempDate = []

print("TAKSIDI in progress...")
for div in soup.find_all('div', attrs={'class':'oneproduct'}):
    print("in loop")
    i += 1
    # for i, n in enumerate(div):
    #     print(i,": ",n)

    # # #

    div_place_where = div.find('h2').get_text()
    print(div)

    if "@" in div_place_where:
        city = div_place_where.split("@")[1].strip()
        # print(city)

    div_where = re.search('@ (.*)|- (.*)', div_place_where)
    #print(div_where)
    # d1 = div_where.group(1)
    # d2 = div_where.group(2)

    try:
        # where.append(div_place_where.strip().split(" - ")[0].split("@")[1])
        where.append(city)
    except IndexError:
        where.append(city)
        # where.append(div_place_where.strip().split(" - ")[0])

    # # # #
    div_country = div.find('div', 'placeProduct').get_text().strip().split(' ')
    # print(div_country)
    try:
        country.append(div_country[1])
    except IndexError:
        country.append(div_country[0])

    # # # #
    div_date = (div.find('div', attrs={'class': 'dateProduct'}).get_text().strip())
    date.append(div_date)
    div_place_date = div_date.split(' - ')
    # print("div_place_date", div_place_date)
    # # # #
    dt = [div.strip() for div in div_place_date][0]
    tempDate.append(dt)
    # print("DT", dt)
    # # # #
    div_price = (div.find('div', attrs={'class': 'priceProductPrice'}).get_text())
    price.append(div_price.strip())
    # # # #
    link = ("https://taksidi.pl" + div.find('a')['href'])
    links.append(link)
    # # # #

for pg in links:
    try:
        response = requests.get(pg, headers=headers)
        res_status = response.status_code

        soup3 = BeautifulSoup(response.content, "html.parser")

        if res_status == 200:
            file = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\taksidifreeslots.html', 'a', encoding="utf8")
            file.write(str(soup3.prettify()))
            file.close()


    except IndexError as exc:
        print('There was a problem with error: {}'.format(exc))

free_slot_file = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\taksidifreeslots.html', encoding="utf8")
soup2 = BeautifulSoup(free_slot_file, "html.parser")
free_slot_file.close()
# poniżej szukam informacji na temat wolnych miejsc
for div in soup2.find_all('table', attrs={'style':'width:100%; margin:10px 0; font-size:18px;'}):
    try:
        freeslot.append(div.get_text("|", strip=True).split("|")[13])
        # print(div.get_text("|", strip=True).split("|")[13])
    except IndexError:
        freeslot.append("Brak danych")
        # print("Brak danych")

for i, slott in enumerate(where):
    store_info = {}

    if where[i] not in "Chorwacja":
        # print("DATE:", date[i].strip(" - ")[0], now)
        if tempDate[i] >= now and tempDate[i] > "2018-12-01":
            store_info = {
                            'Organizator': "TAKSIDI",
                            'City': where[i],
                            'Country': country[i],
                            'Date': date[i],
                            'Price': price[i],
                            'Free slots': slott,
                            'Link': links[i]

                        }

            print("{0}:\n Gdzie: {1} \n Kraj: {2} \n Kiedy: {3}\n Cena: {4}\n Link: {5}\n Wolne miejsca: {6}".
                          format(i, where[i], country[i], date[i], price[i], slott, links[i], '\n'))

            scraped_store_taksidi.append(store_info)

# poniżej otwieram plik json
# with open('taksidi.json', 'w') as json_file:
#     json.dump(scraped_store_taksidi, json_file, indent=4, ensure_ascii=False)
time.sleep(0.2)
# usuwam tymczasowy plik potrzebny do pobrania listy wolnych miejsc
try:
    os.remove(r'C:/Users/PREZES/Desktop/snowridess/venv/html/taksidifreeslots.html')
    print("Plik ""taksidifreeslots.html"" został usunięty pomyślnie.")
    print("TAKSIDI done")
except OSError:
    print(OSError.strerror )
    pass
