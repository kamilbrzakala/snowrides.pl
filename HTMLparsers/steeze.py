from bs4 import BeautifulSoup
from bs4.element import Comment
import re, datetime, json
from collections import OrderedDict

i = 0
data = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\steeze.html', encoding="utf8")

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d")
soup = BeautifulSoup(data, "html.parser")
scraped_store_steeze = []

kraje = {

    'Francja' : ['les 2 alpes','l2a','les deux alpes','val thorens / orelle','val thorens','val thorens / 3 doliny',
                 "tignes / tal d'isere",'tignes','orelle',"val d'isere",'la plagne / paradiski','la plagne',
                 'paradiski','3 doliny','valmeinier',"alpe d'huez",'serre chevalier','puy saint vincent',
                 'les menuires',"saint jean d'arves"],

    'Włochy' : ['marilleva 1400','madonna di campiglio/pinzolo','madonna di campiglio','pinzolo',
                'tonale','ponte di legno','livigno','monte rosa - alagna','monte rosa','alagna'],

    'Austria' : ['schladming'],

    'Chorwacja' : ['sukosan'],

    'Szwajcaria' : ['laax'],

    'Gruzja' : ['gudauri']

}

print("STEEZE in progress...")
try:
    for div in soup.find_all('div', attrs={'class':'trip-desc'}):
        i += 1
        # for i, n in enumerate(div):
        #     print(i,": ",n)


        div_where = div.find('h2').get_text().strip()
        div_wheree = div_where.lower()
        # # #
        div_place_date = div.find('p', attrs={'class': 'info'}).get_text()
        div_date = div_place_date.split('INFO: ')[1].strip()
        # # #
        div_place_price = div.find('p', attrs={'class': 'desc'}).get_text()
        div_price = div_place_price.split('Cena: ')[1].strip()
        # # #
        link = "https://steeze.pl" + div.find('a')['href']
        # # #

        print("{0}:\n Gdzie: {1} \n Kraj: {2} \n Kiedy: {3}\n Cena: {4}\n Link: {5}\n Wolne miejsca: {6}".
              format(i, div_where, "s", div_date, div_price, link, "Brak danych", '\n'))

        store_info = {}
        for key, value in kraje.items():
            if div_wheree in value:
                kraj = key
                store_info = {
                    'Organizator': "STEEZE",
                    'City': div_where,
                    'Country': kraj,
                    'Date': div_date,
                    'Price': div_price,
                    'Free slots': "Brak danych",
                    'Link': link

                }
                print("{0}:\n Gdzie: {1} \n Kraj: {2} \n Kiedy: {3}\n Cena: {4}\n Link: {5}\n Wolne miejsca: {6}".
                      format(i, div_where, kraj, div_date, div_price, link, "Brak danych", '\n'))
        if store_info:
            scraped_store_steeze.append(store_info)
except IOError as e:
    print("Steeze  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

print("STEEZE done")
# with open('steeze.json', 'w') as json_file:
#     json.dump(scraped_store_steeze, json_file, indent=4, ensure_ascii=False)
