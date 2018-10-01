# snowrides.pl

snowrides.pl is my own project developed for own purposes.

snowrides.pl shows parsed data from several winter travel agencies websites.

Basic target is to gather winter trips data in json format: 
{
            "Organizator": "FEELTHEFLOW",
            "City": "Livigno",
            "Country": "Włochy",
            "Date": "07.12.18 - 16.12.18",
            "Price": "1559",
            "Free slots": "PROMO -40 PLN tylko do 19.09",
            "Link": "https://www.feeltheflow.pl/wyjazdy/livigno-hello-winter-vol-1-lux-2"
 }
and show that data in front end.

Json data is converted into csv file and exported into webhost provider's MySQL database.

If you would like to run ths backend, then you have to have installed on your local machine python3.7

By running a script Downloads/MainClass.py
You will run the following 3 scrpts:
1. DownloadWebSitesHTML
2. csvParser
3. csvExportToSQL

If you would like to review the python parser coded of each travel agency then you have to go to HTMLparsers folder.
html folder stores source page's downloaded by the script DownloadWebSitesHTML.

Please notice that you won't be able to upload parsed data into MySQL database because you will have to have account in OVH provider.

From security reason I did not provide my own credentials.
