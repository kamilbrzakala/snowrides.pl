# # #
# 1st. run DownloadWebSitesHTML
# 2nd. run csvParser
# 3rd. run csvImport
# # #


from urllib.error import URLError
import requests, bs4, re, logging, sys, json, os.path
from urllib.request import urlopen, Request
sys.path.insert(0, r'C:\Users\PREZES\Desktop\snowridess\venv\HTMLparsers')
from multiprocessing import Pool




headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

save_path = r'C:\Users\PREZES\Desktop\snowridess\venv\html'

logging.debug('Connected.')


# integra-wyjazdy - next page download
# def responsee(url):
#     try:
#         response = requests.get(url, headers=headers)
#         res_status = response.status_code
#         print(res_status)
#         soup = bs4.BeautifulSoup(response.content, "html.parser")
#         s = soup.find(class_='nicdark_btn nicdark_bg_green medium white nicdark_press')
#         # print(s.get('href'))
#         url = s.get('href')
#         # saving to file
#         if res_status == 200:
#             www = os.path.join(save_path, "integra-wyjazdy.html")
#             file = open(www, 'w')
#             file.write(str(soup.prettify()))
#             file.close()
#         responsee(url)
#     except AttributeError:
#         print("end")

def webScrap(www):

    url = www

    if ('www' not in www):
        www = www.split('/')[2].split('.')[0]
        print(www)
    else:
        www = www.split('.')[1]
        print(www)

    #request
    if www == "zerogravity":
        try:
            # This is the only data required by the api
            # To send back the stores info
            data = {
                'action': 'filter_events'
            }
            # Making the post request
            response = requests.post(url, data=data, headers=headers)

            # The data that we are looking is in the second
            # Element of the response and has the key 'data',
            # so that is what's returned
            res_status = response.status_code
            #res_status2 = response.raise_for_status()
            print(res_status)
            # print(response.raise_for_status())
            soup = bs4.BeautifulSoup(response.content, "html.parser")

            # print(soup.prettify())

            # saving to file
            if res_status == 200:
                www = os.path.join(save_path, www + ".html")
                file = open(www, 'w', encoding='utf-8')
                file.write(str(soup))
                file.close()

        except Exception as exc:
            print('There was a problem with error: {}'.format(exc))

    # elif www == "integra-wyjazdy":
    #
    #      responsee(url)

    else:

        try:
            response = requests.get(url, headers=headers)
            res_status = response.status_code
            res_status2 = response.raise_for_status()
            print(res_status)
            # print(response.raise_for_status())
            soup = bs4.BeautifulSoup(response.content, "html.parser")

            # print(soup.prettify())

            # saving to file
            if res_status == 200:
                www = os.path.join(save_path, www + ".html")
                file = open(www, 'w', encoding='utf-8')
                file.write(str(soup.prettify()))
                file.close()
        except Exception as exc:
            print('There was a problem with error: {}'.format(exc))


tripList = ['http://www.feeltheflow.pl/wyjazdy',
            'http://integra-wyjazdy.pl/wyjazdy/',
            'http://www.shakeit.pl/wyjazdy/wyjazdy-zimowe/',
            'https://snowevents.pl/wyjazdy-na-narty-i-snowboard',
            'https://www.snowmotion.pl/wyjazdy',
            'https://www.snowshow.pl/wyjazdy',
            'http://snowz.pl/wyjazdy.html',
            'http://steeze.pl/wyjazdy',
            'https://www.taksidi.pl/wyjazdy',
            'http://zerogravity.pl/wp-admin/admin-ajax.php'] # zerogravity IMPORTANT to provide a path to ajax.php!!!!

# webScrap('http://zerogravity.pl/wyjazdy/')

for item in tripList:
    webScrap(item)

# p = Pool(5)
# p.map(webScrap, ['http://www.feeltheflow.pl/wyjazdy',
#             'http://integra-wyjazdy.pl/wyjazdy/',
#             'http://www.shakeit.pl/wyjazdy/wyjazdy-zimowe/',
#             'https://snowevents.pl/wyjazdy-na-narty-i-snowboard',
#             'https://www.snowmotion.pl/wyjazdy',
#             'https://www.snowshow.pl/wyjazdy',
#             'http://snowz.pl/wyjazdy.html',
#             'http://steeze.pl/wyjazdy',
#             'https://www.taksidi.pl/wyjazdy',
#             'http://zerogravity.pl/wp-admin/admin-ajax.php'])

from feeltheflow import scraped_store_feeltheflow as feeltheflow
from integra_wyjazdy import scraped_store_integrawyjazdy as integrawyjazdy
from shakeit import scraped_store_shakeit as shakeit
from snowevents import scraped_store_snowevents as snowevents
from snowmotion import scraped_store_snowmotion as snowmotion
from snowshow import scraped_store_snowshow as snowshow
from snowz import scraped_store_snowz as snowz
from steeze import scraped_store_steeze as steeze
# from taksidi import scraped_store_taksidi as taksidi
from zerogravity import scraped_store_zerogravity as zerogravity

trips_json_scraped_store = []
if feeltheflow:
    trips_json_scraped_store.append(feeltheflow)
if integrawyjazdy:
    trips_json_scraped_store.append(integrawyjazdy)
if shakeit:
    trips_json_scraped_store.append(shakeit)
if snowevents:
    trips_json_scraped_store.append(snowevents)
if snowmotion:
    trips_json_scraped_store.append(snowmotion)
if snowshow:
    trips_json_scraped_store.append(snowshow)
if snowz:
    trips_json_scraped_store.append(snowz)
if steeze:
    trips_json_scraped_store.append(steeze)
# if taksidi:
#     trips_json_scraped_store.append(taksidi)
if zerogravity:
    trips_json_scraped_store.append(zerogravity)
#
with open(r'C:\Users\PREZES\Desktop\snowridess\venv\all_trips.json', 'w', encoding="utf8") as json_file:
    json.dump(trips_json_scraped_store, json_file, indent=4,ensure_ascii=False)

logging.debug('Done.')
