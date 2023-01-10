from bs4 import BeautifulSoup
import requests
ICAO = 'EHDL'
VFR_STATUS = "NONE"



def getVfrStatus(ICAO):
    html_text = requests.get('https://www.aviationweather.gov/metar/data?ids='+ICAO+'&format=decoded&hours=0&taf=off&layout=off').text
    soup = BeautifulSoup(html_text, 'lxml')

    raw_data = soup.find_all('td')

    split_vis = raw_data[13].text.split()
    split_ceil = raw_data[15].text.split()
    VIS = int(split_vis[0])
    CEIL = int(split_ceil[0])

    if (VIS >= 5 and (CEIL > 3000)):
        VFR_STATUS = "VFR"
    elif (VIS >= 3 and (CEIL > 1000)):
        VFR_STATUS = "MVFR"
    elif (VIS >= 1 and (CEIL > 500)):
        VFR_STATUS = "IFR"
    elif (VIS < 1 or (CEIL < 500)):
        VFR_STATUS = "LIFR"
    else:
        VFR_STATUS = "NONE"

    #print(ICAO, VFR_STATUS)
    return VFR_STATUS


print(getVfrStatus(ICAO))