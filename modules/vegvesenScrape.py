import base64
import datetime
import json
import threading
import time
from email.mime import base
from os import getcwd, listdir, path

import appdaemon.plugins.hass.hassapi as hass
import ha_version
import requests


class vegvesenScrapeNote(hass.Hass):

    def initialize(self):
        self.log(
            f"🚨 Launching vegvesen-Notify {ha_version.__version__}",
            ascii_encode=False,
        )

    def notifyy(self, event):
        self.log(f"🎇🎆🎆🎆🎆 Something happened", ascii_encode=False)

        self.notify(event["start"],
                    name="mobile_app_mobiln",
                    title=event["oppmotested"])
        self.notify(event["start"],
                    name="mobile_app_sexy_beast",
                    title=event["oppmotested"])
       # will send a message through notify.smtp instead of the default notify.notify


class vegvesen_scraper(hass.Hass):

    def initialize(self):

        self.set_log_level("INFO")
        self.log(
            f"🚨 Launching scraper {ha_version.__version__}",
            ascii_encode=False,
        )
        self.all_classes = []
        timer = datetime.time(0, 0, 0)
        self.run_minutely(self.callback_minutely, timer)

    thresh_date = datetime.datetime(2022, 7, 3)
    cookie_dir = "/config/appdaemon/apps/vegvesen-scraper/const/cookie"

    # parametrene "v", arbeidsflytId, klasse
    newline = "\n"
    params = {"v": 2, "arbeidsflytId": 754821923, "klasse": "B"}
    traffic_stations = [471, 741, 761, 491, 751]
    url = "https://forerett-adapter.atlas.vegvesen.no/provetimer"

    def callback_minutely(self, kwargs):
        self.main()

    def fetch_class(self, station):
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
        s = requests.Session()
        result = s.get(
            params=params,
            url=self.url,
            headers={
                "cookie": decode_cookie()
            }
        )

        if result.status_code != 200:
            self.log("%s\n%s" % (result.text, result.url), log="error_log")
            return result.status_code
        else:
            return result.json()

    def cycle_station(self):
        if self.all_classes:
            # Hjelpefunksjon for å iterere gjennom alle kjørestasjonene
            self.all_classes.clear()
        for station in self.traffic_stations:

            classes = self.fetch_class(station)
            if not classes:
                continue
            elif classes == 401:  # Om responsen fra serveren var 401 så er det antagelig pga. ugyldig autentisering. Send derfor en event til Home Assistant som videre trigger get_cookie-automasjonen
                self.fire_event("cookie_refresh", reauth="true")
                return
            elif classes == 500: # Om responsen fra serveren var 500 ( Intern server-error)
                self.error("Server fucked up somehow")
                continue
            else:
                self.all_classes.append(classes)
        return

    def Sorter(self):
        driving_classes = {}
        for classes in self.all_classes:
            currentStation = classes[0]["oppmotested"].split(" ")[0]
            driving_classes.update({currentStation: []})
            print(classes[0]["oppmotested"])
            for driving_class in classes:
                if driving_class:
                    driving_classes[currentStation].append(
                        driving_class["start"])
                    kjoretime = driving_class["start"]
        return driving_classes

    # Gjør informasjonen leselig for InfluxDB
    def InfluxDBify(self, influxDB=False):
        driving_classes = {}
        for classes in self.all_classes:
            currentStation = classes[0]["oppmotested"].split(" ")[0]
            driving_classes.update({currentStation: []})
            print(classes[0]["oppmotested"])
            for driving_class in classes:
                if driving_class:
                    driving_classes[currentStation].append(
                        driving_class["start"])
                    kjoretime = driving_class["start"]

                    full_string = datetime.datetime.strptime(
                        kjoretime, "%Y-%m-%dT%H:%M:%S")
                    class_date = full_string.strftime("%Y-%m-%dT%H:%M:%SZ")
                    class_time = full_string.strftime("%H:%M:%S")
                    if influxDB:
                        self.push_InfluxDB(
                            currentStation, kjoretime, class_date, class_time)
                    print(class_date, class_time, full_string)
        print(driving_classes)
        return driving_classes

    def push_InfluxDB(self, traffic_station, full_string, date_class, time_class):
        InfluxDB_sync.sendToInfluxDB(
            traffic_station=traffic_station,
            date_class=date_class,
            time_class=time_class,
            full_string=full_string
        )
        # traffic_station,date_class,time_class,datetime_class

    def scheduler(self):
        time_flag = False
        t = threading.Timer(interval=10, function=self.cycle_station)
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
            self.log(trafikkstasjon, level="DEBUG", log="diag_log")
            stasjon_flag = True  # flagg sånn at printen blir finar
            kjoretime_list = []
            
            for kjoretime in trafikkstasjon:
                tid = datetime.datetime.strptime(
                    kjoretime["start"], "%Y-%m-%dT%H:%M:%S")
                if 1 == 1: 
                    if isinstance(trafikkstasjon, list):
                        if stasjon_flag:
                            now = datetime.datetime.now()
                            kjoretime_list.append(f"{self.newline}{kjoretime['oppmotested']} - {now.strftime('%H:%M:%S')}")
                            stasjon_flag = False
                        if tid.day <= 24 and kjoretime['oppmotested'] == "Orkdal trafikkstasjon" and tid.month <= 7:
                            vs = self.get_app("vegvesen-notifier")
                            vs.notifyy(kjoretime) 
                        kjoretime_list.append(kjoretime["start"])
            timer = self.newline.join(str(x) for x in kjoretime_list)
            self.log(f"{timer}", ascii_encode=False)
         #   self.log("="*(len(kjoretime["oppmotested"])+1))
    def bestillTime(self, kjoretime):
        def decode_cookie():
            return base64.b64decode(
                open(self.cookie_dir)
                .read())
        url = "https://forerett-adapter.atlas.vegvesen.no/provetimer?v=2"
        postRequest = json.dumps({
            "arbeidsflytId": str(self.params["arbeidsflytId"]),
            "start": kjoretime["start"],
            "ferdig": kjoretime["ferdig"],
            "oppmotested": kjoretime["oppmotested"],
            "sprakkode": kjoretime["sprakkode"],
            "klasse": self.params["klasse"],
            "trafikkstasjonId": kjoretime["trafikkstasjonId"]
        })
        print(postRequest)
        s = requests.Session()

        o = s.options(
            url=self.url,
            headers={
                "cookie": decode_cookie(),
                "Access-Control-Request-Headers": "content-type,x-selvbetjening-xsrf-token",
                "Access-Control-Request-Method": "POST"
            }

        )
        print(o.headers, o.content)

        p = s.post(
            json=postRequest,
            url=self.url,
            headers={
                "cookies": decode_cookie(),
                "Content-Type": "application/json",
                "SELVBETJENING-XSRF-TOKEN": "212d3b290eaa3bfc4970f4786bbcbb454832c877ccf9ee2e7fc94f36da7d"
            },
            data=postRequest
        )
        self.log(
            f"Result: \n{100*'_'}\n {o.headers} \n \n {p.content} _________")

    """    if s != 200 :
                self.log("%s\n%s" % (s.text,s.url),log="error_log")
                return False
            else:
                return s.json()
                
                """
