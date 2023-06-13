import requests
from bs4 import BeautifulSoup
import time as tm
import pandas as pd
import datetime

def retry_request(url, headers):
    while True:
        try:
            res =requests.get(url, headers=headers) #,data = payload
            return res
        except:
            print("retry")
            tm.sleep(1)
            
# compare current with the leastest one
def compareList(current, least):
    # add: difference in current not in least
    add = list(set(current) - set(least))
    # subtract: difference in least not in current
    subtract = list(set(least) - set(current))
    a = "New vessel(s): {}".format(add) if add else "There is nothing added today ~"
    s = "Delisted vessel(s): {}".format(subtract) if subtract else "There is nothing subtracted today ~"    
    return a,s

def yesterdayDate():
    return str(int(str(datetime.date.today()).replace('-',''))-1)

def todayDate():
    return str(datetime.date.today()).replace('-','')

def readCompare(todayDate, yesterdayDate):
    yesterday = pd.read_csv('C:/Users/User/Desktop/Python/iotc/'+ yesterdayDate+'.csv')
    today = pd.read_csv('C:/Users/User/Desktop/Python/iotc/'+ todayDate+'.csv')
    to = today['IOTC']
    yester = yesterday['IOTC']
    print(compareList(to, yester))

def main():
    try: 
        readCompare(todayDate(), yesterdayDate())
        print("press control+ C to close the window")
        
    except FileNotFoundError:        
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        url = "https://iotc.org/vessels/current?page=0"

        res = retry_request(url,headers)
        soup = BeautifulSoup(res.text, "html.parser")

        number = soup.find("div", {"class": "results"}).get_text().replace(" vessel records found","")

        if int(number) % 20 != 0:
            page = int(number) // 20
        else:
            page = int(number) // 20-1
            
        print("vessel number: {}".format(number), "\npage number: {}".format(page+1) )

        print("today's file is downloading~")
        IOTC = []
        serialHref = []
        vesselName = [] 
        callSign = []

        i = 0
        while i <= page:
            url = 'https://iotc.org/vessels/current?page='+  "{}".format(i)
            res = retry_request(url,headers)
            soup = BeautifulSoup(res.text, "html.parser")
            indexIOTC = soup.find_all('td', class_='views-field views-field-vrvesselkey')
            
            for number in indexIOTC:
                IOTC.append((number.text).replace('\n','').strip())
            
            for div in indexIOTC:
                links = div.select("a:not([class])")
                for link in links:
                    href = link.get("href")
                    serialHref.append('https://iotc.org/vessels/'+ href)
            
            vessel = soup.find_all('td', class_='views-field views-field-vesselname active')
            for name in vessel:
                vesselName.append((name.text).replace('\n','').strip())

            
            ircs = soup.find_all('td', class_='views-field views-field-ircs')
            for n in ircs:
                callSign.append((n.text).replace('\n','').strip())
            i += 1
        print("today's file is completely downloaded\n\
            Please wait for saving~")    
        # write in csv    
        df = pd.DataFrame({'IOTC': IOTC,
                        'vessel': vesselName,
                        'href': serialHref,
                        'callSign': callSign})
        today = str(datetime.date.today()).replace('-','')
        df.to_csv('C:/Users/User/Desktop/Python/iotc/'+today+'.csv', mode='w', index=False)
        readCompare(todayDate(), yesterdayDate())
        print("press control+ C to close the window")

main()    
input()
