# ==============================================================
# Pobierz w Archiwach - Herunterladen aus den Archiven
# --------------------------------------------------------------
# (c) 2021, Clemens Draschba
# ==============================================================
import numpy  as np
import pandas as pd
import xlsxwriter
import re
import sys
import requests
import os
import time
import logging
import multiprocessing.pool as mpool
from bs4 import BeautifulSoup

# Prepare Logging:
logging.basicConfig(format='%(asctime)s|%(name)s|%(levelname)s|%(message)s', level=logging.INFO)
logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
logging.getLogger("numexpr.utils").setLevel(logging.WARNING)

# Read the zespol-ID from command line or throw an error message:
if (len(sys.argv) != 2) :
    print("Error: Invalid number of parameters:", len(sys.argv))
    print("USAGE: pobierzwarchiwach.py zespolid")
    print("Exiting....  Try again please!")
    exit(1)

# ID to download:
zespol    = int(sys.argv[1])
logging.info('Zespol-ID read: {:d}'.format(zespol) )

baseurl   = 'https://www.szukajwarchiwach.gov.pl/de/'
zespolurl = baseurl + 'zespol/-/zespol/{}?_Zespol_javax.portlet.action=zmienWidok&_Zespol_nameofjsp=jednostki&_Zespol_resetCur=false&_Zespol_delta=200'

# =========================================================================================================================
# Function to dowlaod the zip file of one single unit identified by its jednoska id:
def download_scans( unit, chunk_size=4096):
    jednostka = unit.jid
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

    # Check if directory already exists... otherweise create
    if not os.path.exists(unit.path):
        os.makedirs(unit.path)
    
    savefile = unit.path + "/" + unit.file + ".zip"
    nread = 0
    if not os.path.exists(savefile) :
        logging.info("Start downloading Jednostka: {:9d} : {:15s} with {:5d} scans".format(jednoska, unit.signature, unit.scans) )
        t_start = time.time()
        try :
            r = requests.post(url=url, data=reqdata, headers=h, stream=True)
            with open(savefile, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    nread += fd.write(chunk)
            t_end   = time.time()
            t_delta = t_end - t_start
            rate    = 0.001 * nread / t_delta
            logging.info("Done  downloading Jednostka: {:9d} : {:15s} with {:5d} scans to {:s} with {:d} bytes in {:8.3f}[sec] --> {:.3f}[kB/s] ".format(jednoska, unit.signature, unit.scans, savefile, nread, t_delta, rate) )
        except :
            logging.error("An error has occurred! Exiting download for {:s}... deleteing file {:s}".format(unit.signature, savefile))
            if os.path.exists(savefile) :
                os.remove(savefile)
        #print("Done  downloading Jednostka:", jednoska, ':', unit.signature, 'with {:5d}'.format(unit.scans), 'scans to', savefile, "with", nread, "bytes in {:8.3f}[sec] ".format(t_delta) , " --> {:.3f}[kB/s]".format(rate) )
    else :
        logging.info("Skipping existing file {:s} !".format(savefile) )

# end of function
# =========================================================================================================================

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
logging.debug('Retrieving Session: ')
session = requests.Session()
req     = session.get( baseurl, headers=Headers)
cookies = session.cookies;
logging.info("JSessionID = {:s}".format( cookies['JSESSIONID']) )
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
# Find original title of zespol:
jeddtitle  = soup.find("div", {"class":"tytulJednostki"})
origtitle     = jeddtitle.p.string
logging.info("Original Titel: '{:s}'".format(origtitle))

# Find div with table of untis and parse them:
jeddiv    = soup.find("div", {"class": "jednostkaObiekty row"})
jedtable  = jeddiv.table.tbody
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
units['jid']      = units['url'].str.extract('(\d+)').astype(int)
units['archive']  = units['signature'].str.split('/',5).str[0]
units['bestand']  = units['signature'].str.split('/',5).str[1]
units['serie']    = units['signature'].str.split('/',5).str[2]
units['subserie'] = units['signature'].str.split('/',5).str[3]
units['unit']     = units['signature'].str.split('/',5).str[4]
units['path']     = units['archive'].apply(lambda x: x.zfill(2)) + "/" + units['bestand'].apply(lambda x: x.zfill(4))
units['file']     = units['path'] + "/" + units['serie'] + "/" + units['subserie'] + "/" + units['unit'].apply(lambda x: x.zfill(5))
units['file']     = units['file'].str.replace('[^0-9a-zA-Z]+', '_')

units_with_scans = units[units['scans'] > 0 ]
logging.info("List of units with Scans:")
logging.info("------------------------------------------------------------------------------")
print(units_with_scans)

xlswriter = pd.ExcelWriter('xxx.xlsx', engine='xlsxwriter', options={'strings_to_urls': False})
units.to_excel(xlswriter, sheet_name="Units" , encoding="utf-8")
xlswriter.save()
xlswriter.close()

logging.info("------------------------------------------------------------------------------")
for index, unit in units_with_scans.iterrows():
    jednoska = unit.jid
    download_scans(unit)

