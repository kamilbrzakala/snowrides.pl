from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request, re, json,itertools
from collections import OrderedDict

data = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\integra-wyjazdy.html', encoding="utf8")

i = 1
expected_country = ['Francja', 'Ukraina', 'Włochy']
soup = BeautifulSoup(data, "html.parser")
scraped_store_integrawyjazdy = []

print("INTEGRA-WYJAZDY in progress...")
try:
    for div in soup.find_all("div", attrs={'class': 'grid grid_4 percentage nicdark_masonry_item nicdark_padding10 nicdark_sizing'}):
        # for i, n in enumerate(div):
        #    print(i,": ",n)

        div_where = div.find('div', attrs={'class': 'nicdark_textevidence nicdark_bg_yellow'}).get_text().strip()
        div_where = [y for y in (div.strip() for div in div_where.splitlines()) if y][0]
        div_where = [div_where]
        div_country = [div.find('p', attrs={'class': 'white'}).get_text().strip()]
        # div_countryy = [div.find('p', attrs={'class': 'white'}).get_text().strip().lower()]



        # # #
        link = div.find('a', attrs={'class': 'grey nicdark_btn nicdark_border_grey medium nicdark_press'})['href']
        link2 = [div.find('a', attrs={'class': 'grey nicdark_btn nicdark_border_grey medium nicdark_press'})['href']]
        # link = [div.find('a')['href'].strip()]
        # # #
        div_price = div.find('div', attrs={'class': 'nicdark_fadeout nicdark_absolute nicdark_height100percentage nicdark_width_percentage100'}).get_text().strip()
        # div_price = [div_price]
        div_price = [div_price + ", Więcej szczegółów pod linkiem: " + link + "#cena"]
        # print(div_price)
        # # # #
        div_date = [div.find('div', attrs={'class': 'nicdark_focus nicdark_padding1020 nicdark_sizing nicdark_width_percentage50'}).get_text().strip()]
        # print(div_date)

        data = div_country + div_where + div_date + div_price + link2

        str_list = list(set(expected_country) - set(div_country))

        try:
            if data[0] in expected_country:

                print("{0}:\n Gdzie: {1} \n Kraj: {2} \n Kiedy: {3}\n Cena: {4}\n Link: {5}\n".
                      format(i, data[1].split(": ")[1], data[0], data[2], data[3], data[4],  '\n'))

                country_city = data[1].split(" : ")[0]
                store_info = {}
                store_info = {
                    'Organizator': "INTEGRA-WYJAZDY",
                    'City': data[1].split(": ")[1],
                    'Country': data[0],
                    'Date': data[2],
                    'Price': data[3],
                    'Free slots': "Brak danych",
                    'Link': data[4]

                }

                scraped_store_integrawyjazdy.append(store_info)
        except IOError as e:
            print("integra_wyjazdy  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))
        i += 1
except IOError as e:
    print("integra_wyjazdy  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))
print("INTEGRA-WYJAZDY done")

# with open('integra-wyjazdy.json', 'w') as json_file:
#     json.dump(scraped_store_integrawyjazdy, json_file, indent=4, ensure_ascii=False)
