import requests, lxml.html, json
from bs4 import BeautifulSoup
from cachecontrol import CacheControl

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}

url = 'https://phpmyadmin.cluster026.hosting.ovh.net/index.php'
importUrl = "https://phpmyadmin.cluster026.hosting.ovh.net/db_import.php?db=snowridesm278"
queryUrl = "https://phpmyadmin.cluster026.hosting.ovh.net/index.php?db=snowridesm278&target=db_sql.php"



# function for getting hidden input tags

def form(url):
    resp = s.get(url, headers=headers)
    soup = BeautifulSoup(resp.content, 'html.parser')
    data = {e['name']: e.get('value', '') for e in soup.find_all('input', {'name': True})}
    return data



# starting session

s = requests.Session()



# getting hidden input values required for logging

login = s.get(url, headers=headers)
login_html = lxml.html.fromstring(login.text)
hidden_elements = login_html.xpath(r'//form//input[@type="hidden"]')
login_form = {x.attrib["name"]: x.attrib["value"] for x in hidden_elements}



# loading credentials and setting login_parameters for logging

creds = json.load(open(r'C:\Users\PREZES\Desktop\snowridess\venv\myphpadminConnector\creds.txt', encoding="utf8"))
# print("kreds:",creds)
login_form['pma_servername'] = creds['pma_servername']
login_form['pma_username'] = creds['pma_username']
login_form['pma_password'] = creds['pma_password']
login_form['lang'] = 'pl'
# print("LOGIN_FORM: ",login_form)



# sending post request with login_form parameters

response = s.post(url, data=login_form, headers=headers)
# confirm that you are in
# print("\nRESPONSE: ",response.url)



### deleting table trips ###

# getting hidden input values required for deleting

l = s.get("https://phpmyadmin.cluster026.hosting.ovh.net/index.php?db=snowridesm278&target=db_sql.php", headers=headers)
lhtml = lxml.html.fromstring(l.text)
hits = lhtml.xpath(r'//form//input[@type="hidden"]')
data = {x.attrib["name"]: x.attrib["value"] for x in hits}



# creating params

query_form = form(queryUrl)
# print(query_form)
params = {}
# deleting_form['_nocache']='1525879499502529220'
params['ajax_page_request']='true'
params['ajax_request']='true'
params['db']=query_form['db']
fk_checks = {
    0 : 0,
    1 : 1
}
# deleting_form['fk_checks']=fk_checks
params['goto']=query_form['goto']
params['is_js_confirmed']=query_form['is_js_confirmed']
params['message_to_show']=query_form['message_to_show']
params['pos']=query_form['pos']
params['prev_sql_query']=query_form['prev_sql_query']
params['show_query']=query_form['show_query']
params['SQL']=query_form['SQL']
params['sql_delimiter']=query_form['sql_delimiter']
params['sql_query']='drop table trips'
params['table']='trips'
params['token']=query_form['token']



# Confirm that .sql file has been deleted

re = s.get("https://phpmyadmin.cluster026.hosting.ovh.net/db_structure.php?db=snowridesm278", headers=headers)
if "trips" in re.text:
    print("Table \'trips\' will reloaded!")
    re = s.post("https://phpmyadmin.cluster026.hosting.ovh.net/import.php", data=data, params=params, headers=headers)
    status = re.json()['ajax_reload']['reload']
    print("Reloaded: ", status)  ## if you have any troubles, check logs what's being send to webserver
else:
    print("Table \'trips\' doesn't exist.")

### END OF deleting table trips ###


# now we move on to import page and we parse parameters for post request in order to upload trips.sql file

import_form = form(importUrl)
# print("\nIMPORT_FORM: ",import_form)

file = open(r'C:\Users\PREZES\Downloads\trips.sql', 'rb')
files = {'import_file': file}

params = {"ajax_request":"1"}

uploading_form={}



# below are only specific attributes chosen from import_form, those are needed for post request:

uploading_form['noplugin'] = import_form['noplugin']
uploading_form['db'] = import_form['db']
uploading_form['token'] = import_form['token']
uploading_form['import_type'] = import_form['import_type']
uploading_form['csv_new_line']=import_form['csv_new_line']
uploading_form['MAX_FILE_SIZE']=import_form['MAX_FILE_SIZE']
uploading_form['charset_of_file']='utf-8'
uploading_form['allow_interrupt']=import_form['allow_interrupt']
uploading_form['skip_queries']=import_form['skip_queries']
uploading_form['fk_checks']=import_form['fk_checks']
uploading_form['fk_checks']=import_form['fk_checks']
uploading_form['format']='sql'
uploading_form['ods_empty_rows']=import_form['ods_empty_rows']
uploading_form['ods_recognize_percentages']=import_form['ods_recognize_percentages']
uploading_form['ods_recognize_currency']=import_form['ods_recognize_currency']
uploading_form['sql_compatibility']='NONE'
uploading_form['sql_no_auto_value_on_zero']=import_form['sql_no_auto_value_on_zero']
uploading_form['csv_terminated']=import_form['csv_terminated']
uploading_form['csv_enclosed']=import_form['csv_enclosed']
uploading_form['csv_escaped']=import_form['csv_escaped']
uploading_form['csv_new_line']=import_form['csv_new_line']

print("\nUPLOADING_FORM:",uploading_form)



# send post request in order to upload trips.sql file

r = s.post("https://phpmyadmin.cluster026.hosting.ovh.net/import.php", data=uploading_form, files = files, params=params)
r = s.get("https://phpmyadmin.cluster026.hosting.ovh.net/db_structure.php?db=snowridesm278", headers=headers)

# Confirm that .sql file has been uploaded

print("Created table: ", "trips" in r.text)
