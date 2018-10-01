from bs4 import BeautifulSoup
import re, datetime, json


data = open(r'C:\Users\PREZES\Desktop\snowridess\venv\html\shakeit.html', encoding="utf8")

link_result = []
country_result = []
all_trips = []
date_result = []
p_result = []
p_result_without_new_lines = []
p_temporary_result_date = []
p_result_date = []
dt = []
wolne_miejsca_trip = []
free_slots = []
scraped_store_shakeit = []

now = datetime.datetime.now()
now = now.strftime("%d-%m-%Y")
soup = BeautifulSoup(data, "html.parser")

def month_string_to_number(string):
    m = {
        'sty': '01',
        'lut': '02',
        'mar': '03',
        'kwi':'04',
         'maj':'05',
         'czer':'06',
         'lip':'07',
         'sie':'08',
         'wrz':'09',
         'paź':'10',
         'lis':'11',
         'gru':'12'
        }

    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')

print("SHAKEIT in progress...")

try:
    div_place = soup.select('h4[style="color:#fff !important"]')
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    div_price = soup.select('a[class="vc_general vc_btn3 vc_btn3-size-sm vc_btn3-shape-square vc_btn3-style-flat vc_btn3-icon-left vc_btn3-color-grey"]')
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    link = soup.select('h3[style="color: #000000;text-align: left;font-family:Lato;font-weight:900;font-style:normal"]')
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    for h3 in soup.findAll("h3", {"class": "vc_custom_heading"}):
        div_countryy = [y for y in (div.strip() for div in h3.get_text().splitlines()) if y]
        div_country = [div.strip() for div in div_countryy][1]

        if div_country in "Les Deux Alpes":
            div_country = "Francja"
            country_result.append(div_country)
        else:
            country_result.append(div_country.split(', ')[1])

        for a in h3.findAll("a", {"href": True}):
            link_result.append(a["href"])
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    for h in soup.findAll("p"):
        a= h.get_text().strip().splitlines()
        p_result.append(a)
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    for row in p_result:
        a = ''.join([str(elem) for elem in row])
        p_result_without_new_lines.append(a)
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    # wyłapuję tylko wyjazdy w góry
    for i, n in enumerate(p_result_without_new_lines):
        if 'Ferie:' in n:
            p_temporary_result_date.append(n)
        if 'Zakończenie sezonu:' in n:
            p_temporary_result_date.append(n)
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    # wolne miejsca
    for wolne_miejsca in soup.findAll('div', {'class': 'wpb_text_column wpb_content_element '}):
    #   print(wolne_miejsca)
        children = wolne_miejsca.find('p').get_text()
        wolne_miejsca_trip.append([y for y in (div.strip() for div in wolne_miejsca.get_text().splitlines()) if y])
        # print(wolne_miejsca_trip)

    for elems in wolne_miejsca_trip:
        free_slots.append(elems[7])
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    # wycinam datę:
    for p in p_temporary_result_date:
        z = re.findall('\d{1,2}\s+-\s+\d{1,2}\s+(?:[a-zA-Z]ty(?:cznia)?|lut(?:ego)?|mar(?:ca)?|kwi(?:etnia)?|maj(?:a)?|czer(?:wca)?|lip(?:ca)?|sie(?:rpnia)?|wrz(?:e[sś]nia)?|pa[źz](?:dziernika)?|lis(?:topada)?|gru(?:dnia)?)\s+\d{1,4}',p)
        z = [item for z in z for item in z.split(' ')]
        month = month_string_to_number(z[3][:3])
        zz = z[0]+z[1]+z[2]+"."+ month +"."+z[4]
        dtt = z[0]+"-"+ str(month) +"-"+z[4]
        p_result_date.append(zz)
        dt.append(dtt)
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    # tworze string wyjazdu ze wszystkimi szczegolami
    for i, div_where in enumerate(div_place):
        trip = div_where.get_text().strip(), country_result[i], dt[i], div_price[i].get_text().strip(),free_slots[i], link_result[i]
        # dict = {dt[i] : trip}
        all_trips.append(trip)
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    # tworzę słownik wycieczek i terminów wyjazdów
    adict = dict(zip(all_trips,dt))
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))

try:
    for key, value in adict.items():
        # print(value, key)

        valuee = datetime.datetime.strptime(value, "%d-%m-%Y").strftime('%d-%m-%Y')

        newdate1 = datetime.datetime.strptime(valuee, "%d-%m-%Y")
        now1 = datetime.datetime.strptime(now, "%d-%m-%Y")

        if newdate1 > now1:
            # print(key)

            store_info = {}
            store_info = {
                        'Organizator': "SHAKEIT",
                        'City': key[0],
                        'Country': key[1],
                        'Date': key[2],
                        'Price': key[3],
                        'Free slots': key[4],
                        'Link': key[5]
                    }
            scraped_store_shakeit.append(store_info)
except IOError as e:
    print("shakeit  Errors: I/O error({0}): {1}".format(e.errno, e.strerror))



print("SHAKEIT done")
# with open('shakeit.json', 'w') as json_file:
#     json.dump(scraped_store_shakeit, json_file, indent=4,ensure_ascii=False)
