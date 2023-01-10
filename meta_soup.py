from bs4 import BeautifulSoup
import requests
ICAO = ['EDAC',	'EDAH',	'EDBC',	'EDDB',	'EDDC',	'EDDE',	'EDDF',	'EDDG',	'EDDH',	'EDDK',	'EDDL',	'EDDM',	'EDDN',	'EDDP',	'EDDR',	'EDDS',	'EDDV',	'EDDW',	'EDFH',	'EDFM',	'EDGS',	'EDHI',	'EDHK',	'EDHL',	'EDJA',	'EDLN',	'EDLP',	'EDLV',	'EDLW',	'EDMA',	'EDMO',	'EDNY',	'EDQM',	'EDSB',	'EDTL',	'EDTY',	'EDVE',	'EDVK',	'EDXW',	'ETAD',	'ETAR',	'ETEB',	'ETGG',	'ETHA',	'ETHB',	'ETHC',	'ETHF',	'ETHL',	'ETHN',	'ETHS',	'ETIC',	'ETIH',	'ETIK',	'ETMN',	'ETND',	'ETNG',	'ETNH',	'ETNL',	'ETNN',	'ETNS',	'ETNT',	'ETNW',	'ETOU',	'ETSB',	'ETSH',	'ETSI',	'ETSL',	'ETSN',	'ETWM']
VFR_STATUS = "NONE"



def getVfrStatus(ICAO):
    html_text = requests.get('https://www.aviationweather.gov/metar/data?ids='+ICAO+'&format=decoded&hours=0&taf=off&layout=off').text
    soup = BeautifulSoup(html_text, 'lxml')

    raw_data = soup.find_all('td')

    #print(len(raw_data))
    if(len(raw_data) >= 18):
        if(raw_data[15].text == "ceiling and visibility are OK"):
            CEIL = int(10000)
        elif("at least" in raw_data[15].text):
            CEIL = int(12000)
        else:
            split_ceil = raw_data[15].text.split()
            CEIL = int(split_ceil[0])
    else:
        VFR_STATUS = "NONE"
        print(ICAO, VFR_STATUS) 
        return VFR_STATUS

        
    split_vis = raw_data[13].text.split()
    VIS = int(split_vis[0])
    
    

    if (VIS >= 5 and (CEIL > 3000) ):
        VFR_STATUS = "VFR"
    elif (VIS >= 3 and (CEIL > 1000)):
        VFR_STATUS = "MVFR"
    elif (VIS >= 1 and (CEIL > 500)):
        VFR_STATUS = "IFR"
    elif (VIS < 1 or (CEIL < 500)):
        VFR_STATUS = "LIFR"
    else:
        VFR_STATUS = "NONE"

    print(ICAO, VFR_STATUS)    
    #print(ICAO, VFR_STATUS, VIS, CEIL)
    
    return VFR_STATUS


for x in ICAO:
  getVfrStatus(x)