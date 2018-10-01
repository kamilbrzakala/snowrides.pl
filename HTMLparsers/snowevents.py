from bs4 import BeautifulSoup
from bs4.element import Comment
import requests, re, json,os, errno
from collections import OrderedDict
from multiprocessing import Pool

i = 0
data = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\snowevents.html', encoding="utf8")

headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

soup = BeautifulSoup(data, "html.parser")


data = []

div_where = []
div_price = []
div_date = []
links = []
all_trips = []
kraj = []

scraped_store_snowevents = []
temp_list_city = []
freeslot = []

kraje = {

    'Francja' : ['L2A FAMILY','Les 2 Alpes','L2A','Les Deux Alpes','Val Thorens / Orelle','Val Thorens','Val Thorens / 3 Doliny',
                 "Tignes / Val d'Isere",'Tignes','Orelle',"Val d'Isere",'La Plagne / Paradiski','La Plagne',
                 'Paradiski','3 Doliny','Valmeinier',"Alpe d'Huez",'Serre Chevalier','Puy Saint Vincent',
                 'Les Menuires',"Saint Jean D'Arves",'Verbier','Val di Sole', 'Chamrousse', 'Vars-Risoul','Vars',
                 'RISOUL'],

    'Włochy' : ['Marilleva 1400','Madonna di Campiglio/Pinzolo','Madonna di Campiglio','Pinzolo',
                'Tonale','Ponte di Legno','Livigno','Monte Rosa - Alagna','Monte Rosa','Alagna'],

    'Austria' : ['Schladming'],

    'Chorwacja' : ['Sukosan'],

    'Szwajcaria' : ['Laax']

}

# poniżej przeszukuję plik html pobrany snowevents.py
try:
    print("SNOWEVENTS in progress...")
    for div in soup.find_all('div', attrs={'class':'item'}):

        div_where.append(div.find('h4').get_text().split(' - ')[0].strip())

        # this is required to fetch unique cities
        div_wheree = div.find('h4').get_text().split('-')[0].strip()

        temp_list_city.append(div_wheree)
        myset = set(temp_list_city)

        # # #
        div_price.append(div.find('h4').get_text().split(' - ')[1].strip())

        # # #
        div_place_date = div.find('div', attrs={'class': 'item-content'}).get_text()
        div_datee = [y for y in (div.strip() for div in div_place_date.splitlines()) if y]
        div_date.append([div.strip() for div in div_datee][1])

        # # #
        link = div.find('a')['href']
        links.append(link)
        #print(links)
        # # #
        i+=1

        for key, value in kraje.items():
            if div_wheree in value:
                kraj.append(key)

        # print(div_wheree)
except:
    print("SNOWEVENTS: Main div in failed")

print("div_where: ",div_where)
print("div_wheree: ",div_wheree)
print("myset: ",myset)
print("div_price: ",div_price)
print("data: ",div_date)
print("kraj: ", kraj)
# ponizej generuje liste wolnych miejsc per link z listy "links"

if links:
    try:
        print("Creating list of links...")
        for pg in links:
            try:
                print("Searching free slots in progress...")
                response = requests.get(pg, headers=headers)
                res_status = response.status_code
                print(response)
                soup3 = BeautifulSoup(response.content, "html.parser")
                # print(soup3.prettify)
                soup3 = soup3.prettify
                # if res_status == 200:
                file = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\snoweventsfreeslots.html', 'a',encoding="utf8")
                file.write(str(soup3))
                file.close()

            except IndexError as exc:
                print('There was a problem with error: {}'.format(exc))
    except IOError as er:
        print(er)

    try:
        free_slot_file = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\snoweventsfreeslots.html',encoding="utf8")
        soup2 = BeautifulSoup(free_slot_file, "html.parser")
        free_slot_file.close()
    except:
        print(FileNotFoundError)

    # poniżej szukam informacji na temat wolnych miejsc
    try:
        # print("Searching info about free slots")
        for div in soup2.findAll('div', 'vc_general vc_cta3 vc_cta3-style-outline vc_cta3-shape-rounded vc_cta3-align-left vc_cta3-color-skincolor vc_cta3-icon-size-md vc_cta3-actions-right'):
            print("Searching info about free slots...")
            slot = div.find('p')
            if slot:
                s = slot.findNextSibling('p')
                wolne = freeslot.append(s.get_text(" ", strip=True).split(": ")[1])
                # print(wolne)
        # print(freeslot)

        # file = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\snoweventsfreeslotssss.html', 'a',encoding="utf8")
        # file.write(str(freeslot))
        # file.close()
    except:
        print("SNOWEVENTS: Searching info about free slots FAILED")
print("freeslot: ",freeslot)
# poniżej iteruję po liście wolnych miejsc i zapisuje wszystkie dane wycieczki do json-a

try:
    # print("Saving...\n")
    for i, slott in enumerate(freeslot):
        # print("Saving json...\n")

        store_info = {}
        store_info = {
                            'Organizator': "SNOWEVENTS",
                            'City': div_where[i],
                            'Country': kraj[i],
                            'Date': div_date[i],
                            'Price': div_price[i],
                            'Free slots': slott,
                            'Link': links[i]

                    }

        print("{0}:\n Gdzie: {1} \n Kraj: {2} \n Kiedy: {3}\n Cena: {4}\n Link: {5}\n Wolne miejsca: {6}".
                          format(i, div_where[i], kraj[i], div_date[i], div_price[i], links[i], slott,'\n'))

        scraped_store_snowevents.append(store_info)


except IOError as er:
    print(er)
    print("SNOWEVENTS: Creation of json content FAILED")

# poniżej otwieram plik json
try:
    with open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\snowevents.json', 'w') as json_file:
        json.dump(scraped_store_snowevents, json_file, indent=4, ensure_ascii=False)
except:
    print("SNOWEVENTS: Saving json to file FAILED")

# usuwam tymczasowy plik potrzebny do pobrania listy wolnych miejsc
try:
    os.remove(r'C:\Users\PREZES\Desktop\snowridess\venv\html\snoweventsfreeslots.html')
    print("Plik ""snoweventsfreeslots.html"" został usunięty pomyślnie.")
except OSError:
    print(OSError,"\nNie znaleziono bądź nie usunięto pliku snoweventsfreeslots.html")
    pass

print("\nSNOWEVENTS done")
