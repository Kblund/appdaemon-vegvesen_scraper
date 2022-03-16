from modules.vegvesenScrape import vegvesen_scraper
import time
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

    INTERVAL_TIMER = 60/2 # Endre for å justere tid mellom forespørsler
   
    def __init__(self):
        last_time = 0
        new_flag = False
        current_classes = []
        current_vs : vegvesen_scraper

    def scheduler(self):
        time_flag = False
        
        while True:
            
            if not time_flag:
                self.last_time = time.time()
                time_flag = True
            current_time = time.time()
            if (current_time - self.last_time ) < self.INTERVAL_TIMER:
                time_flag = False
                self.hentKjoretimer()
            time.sleep(self.INTERVAL_TIMER)
    
    def hentKjoretimer(self):
        self.current_vs = vegvesen_scraper()
        self.current_classes = self.current_vs.all_classes
        self.new_flag = True
        return

    def compareClasses(self):
        k = 0
    def dateExtractor(self): # Tar imot output fra hentKjoretimer()
        
        if self.new_flag:
            parsed = self.current_vs().parse_dict()
            print(parsed)
        else:
            return
    