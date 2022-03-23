import appdaemon.plugins.hass.hassapi as hass
import ha_version
from os import path

class vegvesenScrapeNote(hass.Hass):

        def initialize(self):
            self.log(path.os.listdir("/config/appdaemon/apps/vegvesen-scraper/const"))
            self.log(  
                f"🚨 Launching vegvesen-scraper {ha_version.__version__}",
                ascii_encode=False,
           )
           
           
            from vegvesenScrape import vegvesen_scraper
            vs = vegvesen_scraper()
            vs.loop()
        def notify(self,event):
            self.log(f"🎇🎆🎆🎆🎆 Something happened", ascii_encode=False)
    
            self.notify(event["start"], title = event["oppmotested"], name = "mobile_app_kenneth_sin_iphone")
           # will send a message through notify.smtp instead of the default notify.notify
            
 
