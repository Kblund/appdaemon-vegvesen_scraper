from email.mime import base
import appdaemon.plugins.hass.hassapi as hass
import json, requests, time, base64, datetime
from os import path
import ha_version
import threading
import time 



class vegvesenScrapeNote(hass.Hass):

        def initialize(self):
            self.log(  
                f"🚨 Launching vegvesen-Notify {ha_version.__version__}",
                ascii_encode=False,
           )
            

           
           
        def notifyy(self,event):
            self.log(f"🎇🎆🎆🎆🎆 Something happened", ascii_encode=False)
    
            self.notify( event["start"], 
            name = "mobile_app_mobiln",
            title = event["oppmotested"])
            self.notify( event["start"], 
            name = "mobile_app_galaxy_watch4_classic_4xwd",
            title = event["oppmotested"])
           # will send a message through notify.smtp instead of the default notify.notify
            
 


class vegvesen_scraper(hass.Hass):
    
        def initialize(self):
            self.log(  
                f"🚨 Launching scraper {ha_version.__version__}",
                ascii_encode=False,
           )
            self.all_classes = []
            timer = datetime.time(0, 0, 0)
            self.run_minutely(self.callback_minutely, timer)
        
        thresh_date = datetime.datetime(2022,3,25)
        cookie_dir = "/config/appdaemon/apps/vegvesen-scraper/const/cookie"
        
        params = {"v":2,"arbeidsflytId":452606344,"klasse":"B"} # parametrene "v", arbeidsflytId, klasse
        traffic_stations=[471,741,761,491,751]
        url = "https://forerett-adapter.atlas.vegvesen.no/provetimer"

        def callback_minutely(self, kwargs):
            self.main()


        def fetch_class(self,station):
            def decode_cookie():
                return base64.b64decode(                                                       
                    open(self.cookie_dir)
                    .read())

            """
            I denne delen setter jeg sammen 'params'-headerne med en kryptert cookie, hentet fra nettleser
            Deretter spør jeg nettsia om å sjå ledige tima
              
            """
            params = self.params                
            params.update(trafikkstasjonId=station)
            res = requests.get(
                params = params,
                url=self.url ,
                headers={
                    "cookie": decode_cookie() 
                    }
               )

            if res.status_code != 200 :
                self.log("%s\n%s" % (res.text,res.url),log="error_log")
                return False
            else:
                return res.json()

        def cycle_station(self):
            if self.all_classes:
                self.all_classes.clear()                                    # Hjelpefunksjon for å iterere gjennom alle kjørestasjonene
            for station in self.traffic_stations:
                
                classes = self.fetch_class(station)
                if not classes:
                    continue
                else:
                  self.all_classes.append(classes)
            return

        def Sorter(self):
            driving_classes = {}
            for classes in self.all_classes:
                currentStation = classes[0]["oppmotested"].split(" ")[0]
                driving_classes.update({currentStation:[]})
                print(classes[0]["oppmotested"])
                for driving_class in classes:
                    if driving_class:
                        driving_classes[currentStation].append(driving_class["start"])
                        kjoretime = driving_class["start"]
            return driving_classes

        def InfluxDBify(self,influxDB = False):                                               # Gjør informasjonen leselig for InfluxDB
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

        
        def scheduler(self):
            time_flag = False
            t = threading.Timer(interval = 10,function =self.cycle_station)
            t.daemon = True
            t.start()
            t.join()
            
        def is_running(self):
            message = \
                """
            still running..
                """
            now = datetime.datetime.now()
            if now.minute % 20 == 0:

                self.log(message)
        def main(self):
            starttime = time.time()
    
            clear = "\n" * 2
            self.is_running()
            self.cycle_station()
            for trafikkstasjon in self.all_classes:
                self.log(trafikkstasjon,level= "DEBUG", log="diag_log")
                stasjon_flag = True # flagg sånn at printen blir finar
                for kjoretime in trafikkstasjon:
                    
                    tid = datetime.datetime.strptime(kjoretime["start"], "%Y-%m-%dT%H:%M:%S")
                    if tid >= self.thresh_date\
                    and tid.month == 3\
                    and kjoretime["oppmotested"] == "Orkdal trafikkstasjon":
                        if isinstance(trafikkstasjon,list):
                            if stasjon_flag: 
                    
                                now =  datetime.datetime.now()
                                self.log(
                                    kjoretime["oppmotested"],
                                    ascii_encode=False
                                )

                                self.log(now.strftime("%H:%M:%S")
                                      )
                                stasjon_flag = False
                            if tid.day >= 28 and kjoretime['oppmotested'] == "Orkdal trafikkstasjon":
                                vs = self.get_app("vegvesen-notifier")
                                vs.notifyy(kjoretime)
                            self.log(kjoretime["start"])
                                    
             #   self.log("="*(len(kjoretime["oppmotested"])+1))