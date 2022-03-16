from email.mime import base
import json, requests, time, base64, datetime
from modules import InfluxDB_sync
from os import path





class vegvesen_scraper:
        params = {"v":2,"arbeidsflytId":452606344,"klasse":"B"} # parametrene "v", arbeidsflytId, klasse
        traffic_stations=[471,741,761,491,751]
        url = "https://forerett-adapter.atlas.vegvesen.no/provetimer"

        def __init__(self):
            self.all_classes = []

            self.cycle_station()    

        def fetch_class(self,station):
            def decode_cookie():
                return base64.b64decode(                                                       
                    open(r"./const/cookie")
                    .read())

            """
            I denne delen setter jeg sammen 'params'-headerne med en kryptert cookie, hentet fra nettleser
            Deretter spør jeg nettsia om å sjå ledige tima
              
            """
            params = self.params                
            params.update(trafikkstasjonId=station)
            res = requests.get(params = params,url=self.url ,headers=dict(cookie=decode_cookie()))
            if res.status_code != 200 :
                print(res.text,res.url)
                return False
            else:
                return res.json()

        def cycle_station(self):                                    # Hjelpefunksjon for å iterere gjennom alle kjørestasjonene
            for station in self.traffic_stations:
                classes = self.fetch_class(station)
                if classes:
                  self.all_classes.append(classes)
                
        def parse_dict(self,influxDB = False):                                               # Gjør informasjonen leselig for InfluxDB
            driving_classes = {}
            for classes in self.all_classes:
                currentStation = classes[0]["oppmotested"].split(" ")[0]
                driving_classes.update({currentStation:[]})
                print(classes[0]["oppmotested"])
                for driving_class in classes:
                    if driving_class:
                        driving_classes[currentStation].append(driving_class["start"])
                        kjoretime = driving_class["start"]
                        
                        full_string = datetime.datetime.strptime(kjoretime,"%Y-%m-%dT%H:%M:%S")
                        class_date = full_string.strftime("%Y-%m-%dT%H:%M:%SZ")
                        class_time = full_string.strftime("%H:%M:%S")
                        if influxDB:
                            self.push_InfluxDB(currentStation,kjoretime,class_date,class_time)
                        print(class_date, class_time, full_string)
            print(driving_classes)
            return driving_classes


        def push_InfluxDB(self, traffic_station, full_string, date_class, time_class):
            InfluxDB_sync.sendToInfluxDB(
                traffic_station = traffic_station, 
                date_class = date_class, 
                time_class = time_class, 
                full_string = full_string
                )
            #traffic_station,date_class,time_class,datetime_class
