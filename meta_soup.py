from bs4 import BeautifulSoup
import requests
import random
import time
from datetime import datetime

from paho.mqtt import client as mqtt_client

ICAO = ['EDAC',	'EDAH',	'EDBC',	'EDDB',	'EDDC',	'EDDE',	'EDDF',	'EDDG',	'EDDH',	'EDDK',	'EDDL',	'EDDM',	'EDDN',	'EDDP',	'EDDR',	'EDDS',	'EDDV',	'EDDW',	'EDFH',	'EDFM',	'EDGS',	'EDHI',	'EDHK',	'EDHL',	'EDJA',	'EDLN',	'EDLP',	'EDLV',	'EDLW',	'EDMA',	'EDMO',	'EDNY',	'EDQM',	'EDSB',	'EDTL',	'EDTY',	'EDVE',	'EDVK',	'EDXW',	'ETAD',	'ETAR',	'ETEB',	'ETGG',	'ETHA',	'ETHB',	'ETHC',	'ETHF',	'ETHL',	'ETHN',	'ETHS',	'ETIC',	'ETIH',	'ETIK',	'ETMN',	'ETND',	'ETNG',	'ETNH',	'ETNL',	'ETNN',	'ETNS',	'ETNT',	'ETNW',	'ETOU',	'ETSB',	'ETSH',	'ETSI',	'ETSL',	'ETSN',	'ETWM']
ICAO = ['EDDR','ETAR','EDFH','EDDF','EDFM','EDSB','EDDS','EDTY','ETHN']

VFR_STATUS = "NONE"

# current date and time


def getVfrStatus(ICAO):
    now = datetime.utcnow()
    html_text = requests.get('https://www.aviationweather.gov/metar/data?ids='+ICAO+'&format=decoded&hours=0&taf=off&layout=off').text
    time.sleep(0.5)
    soup = BeautifulSoup(html_text, 'lxml')

    raw_data = soup.find_all('td')

    split_time = raw_data[3].text.split()
    meta_date = split_time[1][0:2]
    meta_hour = split_time[1][2:4]
    meta_minute = split_time[1][4:6]


    t1 = datetime(year=2023, month=1, day=int(meta_date), hour=int(meta_hour), minute=int(meta_minute))
    print(t1)
    t2 = datetime(year=2023, month=1, day=int(now.strftime("%d")), hour=int(now.strftime("%H")), minute=int(now.strftime("%M")))
    print(t2)

    time_diff = t2 - t1
    #print("Zeitdifferenz:")
    print(time_diff.total_seconds())
 
    s1 = now.strftime("%m/%d/%Y, %H:%M:%S")
    # mm/dd/YY H:M:S format
    #print("s1:", s1)
 

    #print(len(raw_data))
    if(time_diff.total_seconds() < 86400):
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
    else:
        VFR_STATUS = "NONE"
        print(ICAO, VFR_STATUS) 
        return VFR_STATUS
    
    split_vis = raw_data[13].text.split()
    VIS = float(split_vis[0])
    
    

    if (VIS >= 5 and (CEIL > 3000) ):
        VFR_STATUS = "VFR"
    elif (VIS >= 3 and (CEIL > 1000)):
        VFR_STATUS = "MVFR"
    elif (VIS >= 1 and (CEIL >= 500)):
        VFR_STATUS = "IFR"
    elif (VIS < 1 or (CEIL <= 500)):
        VFR_STATUS = "LIFR"
    else:
        VFR_STATUS = "NONE"

    #print(ICAO, VFR_STATUS)    
    print(ICAO, VFR_STATUS, VIS, CEIL)
    
    return VFR_STATUS

broker = '10.10.11.151'
port = 1883

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
# username = 'emqx'
# password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    #client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client, airports_count, status):
    while True:
        if status == "VFR":
            msg = f"0,255,0"
        if status == "MVFR":
            msg = f"0,0,255"
        if status == "IFR":
            msg = f"255,0,0"
        if status == "LIFR":
            msg = f"255,0,255"
        if status == "NONE":
            msg = f"0,0,0"
        #time.sleep(1)
        topic = "cmnd/weathermap/led"+str(airports_count)
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            #print(f"Send `{msg}` to topic `{topic}`")
            return
        else:
            print(f"Failed to send message to topic {topic}")
            return



def run():
    client = connect_mqtt()
   # client.loop_start()
    airports_count = 1
    for x in ICAO:
        status = getVfrStatus(x)
        publish(client, airports_count, status)
        airports_count += 1


if __name__ == '__main__':
    run()

#pip3 install paho-mqtt
#sudo pip3 install rpi_ws281x
#sudo pip3 install adafruit-circuitpython-neopixel
#sudo python3 -m pip install --force-reinstall adafruit-blinka
