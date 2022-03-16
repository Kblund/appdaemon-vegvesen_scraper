from modules.vegvesenScrape import vegvesen_scraper
import time, threading
"""
Bruk fetch_class og cycle_station fra vegvesen_scraper for å hent informasjonen i tidsintervella

Deretter, sammenlign datoan fra alle kjøretiman med dem innjafor 

En del av programmet ser alltid etter kjøretimer.

 hvis programmet finner en kjøretime til ønsket tidspunkt
(innenfor ei tidsramme mellom 22.03 - 05.04 )
book timen. 

Om det skull oppstå det kjæm en time som e nærmar den 31.mars, t tross for at æ har booka

avbestill time, book ny

Er annja program t å booke/avbestill


"""
class KjoretimeListener:
    PREFERED_DATE ="31-03"
    INTERVAL_TIMER = 60/2 # Endre for å justere tid mellom forespørsler
   
    def __init__(self):
        last_time = 0
        new_flag = False
        current_classes : list
        current_vs : vegvesen_scraper

    def scheduler(self):
        time_flag = False
        t = threading.Timer(interval = 10,function =self.hentKjoretimer)
        t.start()
        t.join()
        
    
    def hentKjoretimer(self):
        print("Test")
        vv = vegvesen_scraper()
        print(vv.all_classes)
    def compareClasses(self):
        k = 0
    def dateExtractor(self): # Tar imot output fra hentKjoretimer()
        
        if self.new_flag:
            parsed = self.current_vs().parse_dict()
            print(parsed)
        else:
            return

    def dateExtractor(self,class_list): # Tar imot output fra hentKjoretimer()
        
        if self.new_flag:
            parsed = self.current_vs().InfluxDBify()
            

    def kryperCookie(self):
        import subprocess, base64
        cookie_file = b".\const\cookie"
        cookie = open(cookie_file).read()[8:]
        encoded_cookie = base64.b64encode(cookie.encode("utf-8"))
        open(cookie_file,"w").write(encoded_cookie.decode("utf-8"))
        
    
