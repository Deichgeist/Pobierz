# ==============================================================
# Pobierz w Archiwach - Herunterladen aus den Archiven
# --------------------------------------------------------------
# (c) 2021, Clemens Draschba
# ==============================================================
import numpy  as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

# Alt-Ukta:
zespol    = 111067

baseurl   = 'https://www.szukajwarchiwach.gov.pl/de/'
zespolurl = baseurl + 'zespol/-/zespol/{}?_Zespol_javax.portlet.action=zmienWidok&_Zespol_nameofjsp=jednostki&_Zespol_resetCur=false&_Zespol_delta=200'

# Function to dowlaod the zip file of one single unit identified by its jednoska id:
def download_scans( jednostka, chunk_size=4096):
    url  = baseurl + "jednostka?p_p_id=Jednostka&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=pobierzSkany&p_p_cacheability=cacheLevelPage&_Jednostka_id_jednostki=" + str(jednostka)
    reqdata = {
        "_Jednostka_wyborSkanow": "wszystkie",
        "_Jednostka_skan_IdPliku": "0",
        "_Jednostka_checkboxNames": "skan_IdPliku"
    }
    h = {
       "Content-Type":  "application/x-www-form-urlencoded",
       "Origin":        "https://www.szukajwarchiwach.gov.pl",
       "Referer":       "https://www.szukajwarchiwach.gov.pl/de/jednostka/-/jednostka/"+str(jednostka)
    }
    r = requests.post(url=url, data=reqdata, headers=h, stream=True)
    save_path = str(jednostka) + ".zip"
    nread = 0
    with open(save_path, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=chunk_size):
            fd.write(chunk)
            nread += chunk_size
    return nread

# Request-Headers:
Headers = {
    'Access-Control-Allow-Origin':      '*',
    'Access-Control-Allow-Methods':     'GET',
    'Access-Control-Allow-Headers':     'Content-Type',
    'Access-Control-Max-Age':           '3600',
    'User-Agent':                       'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
	'Accept':                           "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	'Accept-Encoding':                  "gzip, deflate",
	'Accept-Language':                  "de,en-US;q=0.7,en;q=0.3",
	'Cache-Control':                    "no-cache",
	'Connection':                       "keep-alive",
	'DNT':                              "1",
	'Host':                             "www.szukajwarchiwach.gov.pl",
	'Pragma':                           'no-cache'
}
    
# Doing a very first call to baseurl to retrieve a valid Session-ID:
print('Retrieving Session: ')
session = requests.Session()
req     = session.get( baseurl, headers=Headers)
cookies = session.cookies;
print("JSessionID=", cookies['JSESSIONID'])
#print('Cookies=', cookies.get_dict())

#Assembling the request for the list of units:
url     = zespolurl.format(zespol)
p_id    = "ZespolyWeb_INSTANCE_zEpUTaJhvA5o";
params  = {
  "p_p_id":                 p_id,
  "p_p_lifecycle":          "0",
  "p_p_state":              "normal",
  "p_p_mode":               "view",
  "_" + p_id + "_delta":    "500",
  "_" + p_id + "_resetCur": "false",
  "_" + p_id + "_cur":      "1"
}
req      = session.get(url, data=params)
soup     = BeautifulSoup(req.content, 'html.parser')
jeddiv   = soup.find("div", {"class": "jednostkaObiekty row"})
jedtable = jeddiv.table.tbody

unitslist = []
for trow in jedtable("tr") :
    tds = trow('td')
    href     = tds[0].a['href']
    signatur = tds[0].string
    titel    = tds[1].string
    laufzeit = tds[2].string
    scans    = tds[3].string
    unit     = {
        'jid':      0,
        'signature': signatur,
        'title':    titel,
        'years': laufzeit,
        'scans':    int(scans),
        'url':     href
    }
    unitslist.append(unit)

units = pd.DataFrame(unitslist)
units['jid'] = units['url'].str.extract('(\d+)').astype(int)
units_with_scans = units[units['scans'] > 0 ]
print("List of units with Scans:")
print("------------------------------------------------------------------------------")
print(units_with_scans)

for index, unit in units_with_scans.iterrows():
    jednoska = unit.jid
    print("Start Downloading Jednostka: ", jednoska, '  ', unit.signature, ' with ', unit.scans, ' scans:' )
    bytes = download_scans(jednoska)
    print("Done: Bytes written:", bytes);