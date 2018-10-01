from bs4 import BeautifulSoup
from bs4.element import Comment
import re, datetime, json
from collections import OrderedDict

i = 0
data = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\snowmotion.html', encoding="utf8")

now = datetime.datetime.now()
now = now.strftime("%Y-%m-%d")
soup = BeautifulSoup(data, "html.parser")
scraped_store_snowmotion = []
div_where =''
trips = []
kraj = ''

kraje = {

    'Francja' : ['Les 2 Alpes','L2A','Les Deux Alpes','Val Thorens / Orelle','Val Thorens','Val Thorens / 3 Doliny',
                 "Tignes / Val d'Isere",'Tignes','Orelle',"Val d'Isere",'La Plagne / Paradiski','La Plagne',
                 'Paradiski','3 Doliny','Valmeinier',"Alpe d'Huez",'Serre Chevalier','Puy Saint Vincent',
                 'Les Menuires',"Saint Jean D'Arves"],

    'Włochy' : ['Marilleva 1400','Madonna di Campiglio/Pinzolo','Madonna di Campiglio','Pinzolo',
                'Tonale','Ponte di Legno','Livigno','Monte Rosa - Alagna','Monte Rosa','Alagna'],

    'Austria' : ['Schladming'],

    'Chorwacja' : ['Sukosan'],

    'Szwajcaria' : ['Laax']

}

print("SNOWMOTION in progress...")
try:
    for div in soup.find_all('div', attrs={'class':'col-md-3 col-sm-6 col-xs-12 padding_mini2'}):
        i += 1
        # for i, n in enumerate(div):
        #     print(i,": ",n)

        #
        div_place_where = div.find('h2', class_ = 'title')#.get_text()
        # # #
        div_wheree = [text for text in div_place_where.stripped_strings][1].strip()
        div_where = re.findall('([A-Z][a-z1-9].+)',div_wheree)
        if div_where:
            div_where = div_where[0]
        else:
            div_where = div_wheree

        if "PSV" in div_where:
            div_where = 'Puy Saint Vincent'
        elif "L2A" in div_where:
            div_where = 'Les 2 Alpes'
        elif " PREMIUM" in div_where:
            div_where = div_where.split(" PREMIUM")[0]
        else:
            div_where = div_where.split('(', 1)[0].rstrip()
        div_where = div_where.split('(', 1)[0].rstrip() # tu zostaje jeden "(3 DOLINY) " po usunieciu PREMIUM z ((3 DOLINY) PREMIUM) wiec to usuwa ostatni item w nawiasach

        # # #
        div_place_date = div.find('div', attrs={'style': 'padding-left:10px;'}).get_text()
        div_datee = [y for y in (div.strip() for div in div_place_date.splitlines()) if y]
        div_date = [div.strip() for div in div_datee][1]
        # # #
        div_price = [div.strip() for div in div_datee][5]
        # # #
        link = "https://www.snowmotion.pl" + div.find('a')['href']
        # # #
        free_slot = [div.strip() for div in div_datee][3]
        # # #
        if div_date >= now:


            store_info = {}
            for key, value in kraje.items():
              if div_where in value:
                kraj = key
                store_info = {
                    'Organizator': "SNOWMOTION",
                    'City': div_where,
                    'Country': kraj,
                    'Date': div_date,
                    'Price': div_price,
                    'Free slots': free_slot,
                    'Link': link

                }
                print("{0}:\n Gdzie: {1} \n Kraj: {2} \n Kiedy: {3}\n Cena: {4}\n Link: {5}\n Wolne miejsca: {6}".
                      format(i, div_where, kraj, div_date, div_price, link, free_slot, '\n'))


            if store_info:
                scraped_store_snowmotion.append(store_info)
                
except IOError as e:
    print("snowmotion  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))


print("SNOWMOTION done")
with open('snowmotion.json', 'w') as json_file:
    json.dump(scraped_store_snowmotion, json_file, indent=4, ensure_ascii=False)
