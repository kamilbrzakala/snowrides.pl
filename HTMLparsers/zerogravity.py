from bs4 import BeautifulSoup

import urllib.request, re, json
from collections import OrderedDict

i = 0
scraped_store_zerogravity = []
trips = []
kraj = ''

data = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\zerogravity.html', encoding="utf8")

kraje = {

    'Francja' : ['Les 2 Alpes','Les Deux Alpes','Val Thorens / Orelle',"Tignes / Val d'Isere",
                 'Val Thorens','Tignes','Orelle',"Val d'Isere",'La Plagne / Paradiski','La Plagne','Paradiski',
                 'Val Thorens / 3 Doliny','3 Doliny','Valmeinier'],

    'Włochy' : ['Marilleva 1400','Madonna di Campiglio/Pinzolo','Madonna di Campiglio','Pinzolo',
                'Tonale','Ponte di Legno','Livigno','Monte Rosa - Alagna','Monte Rosa','Alagna'],

    'Austria' : ['Schladming'],

    'Chorwacja' : ['Sukosan'],

    'Szwajcaria' : ['Laax']

}

soup = BeautifulSoup(data, "html.parser")

try:
    divs = soup.find_all('div', attrs={'class': 'event-filtered'})
    if divs:
        for div in divs:

             # for i, n in enumerate(div):
               #    print(i,": ",n)

            try:
                 div_where = div.find('p', attrs={'class': 'event-region'}).get_text().strip()
            except AttributeError:
                div_where = 'null'
                pass

            # div_where = div_where.strip()
            # print(div_where)
            div_price = div.find('p', attrs={'class': 'jumbo-price'}).get_text()
            # # #
            div_place_date = div.find('p', attrs={'class': 'event-date'}).get_text().strip()
            div_dte = re.match('(\d\d.\d\d.\d\d\d\d)(?:\s\s+)( - \d\d.\d\d.\d\d\d\d)', div_place_date)
            div_date = div_dte.group(1)+div_dte.group(2)
            # # #
            link = div.find('a')['href']
            # # # Wolne miejsca:
            last_slots = div.find('ul', attrs={'class': 'special-elements'}).get_text()
            lst = [y for y in (div.strip() for div in last_slots.splitlines()) if y]
            # # #
            if not lst:
                lst.append("SĄ MIEJSCA")
            # # #

            for key, value in kraje.items():
                if div_where == 'null':
                    kraj = 'null'
                elif div_where in value:
                    kraj = key
                        # trip = div_where, kraj, div_date, div_price, link, lst[0]
                        # trips.append(trip)
                        # trips
            i += 1

            # print("{0}:\n Gdzie: {1} \n Kiedy: {2}\n Cena: {3}\n Link: {4}\n Wolne miejsca: {5}".
            #        format(i, div_where, kraj, div_date, div_price, link, lst[0], '\n'))

            store_info = {}
            store_info = {
                        'Organizator': "ZEROGRAVITY",
                        'City': div_where,
                        'Country': kraj,
                        'Date': div_date,
                        'Price': div_price,
                        'Free slots': lst[0],
                        'Link': link

            }

            scraped_store_zerogravity.append(store_info)
except IOError as e:
    print("zerogravity Errors: I/O error({0}): {1}".format(e.errno, e.strerror))


# with open('zerogravity.json', 'w') as json_file:
#     json.dump(, json_file, indent=4, ensure_ascii=False)
