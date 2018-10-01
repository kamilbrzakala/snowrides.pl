from bs4 import BeautifulSoup
from bs4.element import Comment
import re, json

i = 1
data = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\snowshow.html', encoding="utf8")

soup = BeautifulSoup(data, "html.parser")

div = soup.find('div', attrs={'class':'trips-collection ss-mobile-collection'})
kontener = re.findall(r'<div class="(ss-trip ss-trip--list.*?)"',str(div))

index = 0
scraped_store_snowshow = []

def remove_duplicates(l):
    return list(set(l))

items = remove_duplicates(kontener)

#for i, n in enumerate(kontener):
#    print(i,": ",n)

print("SNOWSHOW in progress...")
try:
    for item in items:
        # print('\n',item+':','\n')
        for div in soup.find_all('div', attrs={'class':item}):

            div_place = div.find('div').get_text()
            # # #
            div_placee = [y for y in (div.strip() for div in div_place.splitlines()) if y]
            # # #
            div_where = [div.strip() for div in div_placee][0].split('-')[1].strip()
            # # #
            div_country = [div.strip() for div in div_placee][0].split('-')[0]
            # # #
            div_date = [div.strip() for div in div_placee][2]
            # # #
            div_price = [div.strip() for div in div_placee][5]
            # # #
            free_slots = div_placee[3]
            # # #
            link = "https://www.snowshow.pl" + div.find('a')['href']
            # # #


            i += 1


            store_info = {}
            store_info = {
                'Organizator': "SNOWSHOW",
                'City': div_where,
                'Country': div_country,
                'Date': div_date,
                'Price': div_price,
                'Free slots': free_slots,
                'Link': link

            }

            # print("{0}:\n Gdzie: {1} \n Kraj: {2} \n Kiedy: {3}\n Cena: {4}\n Wolne Miejsca: {5} \n Link: {6}".
            # format(i, div_where,div_country, div_date, div_price, free_slots, link + '\n'))

            scraped_store_snowshow.append(store_info)
except IOError as e:
    print("snowshow  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))


print("SNOWSHOW done")
    # poniżej otwieram plik json
    # with open('snowshow.json', 'w') as json_file:
    #     json.dump(scraped_store_snowshow, json_file, indent=4, ensure_ascii=False)
